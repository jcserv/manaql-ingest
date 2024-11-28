import multiprocessing as mp
import os
from abc import ABC, abstractmethod
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from database.models.scryfall_card import ScryfallCard
from django.db import connections, transaction
from tqdm import tqdm


def filterCard(scryfall_card: Dict) -> bool:
    if scryfall_card.get("lang", None) != "en":
        return True
    if scryfall_card.get("layout", "") != "normal":
        return True
    if "paper" not in scryfall_card.get("games", []):
        return True
    return False


def process_card(card: Dict) -> Tuple[bool, bool, Optional[Dict]]:
    """Process a single card and return success, filtered, and failure info."""
    if filterCard(card):
        return False, True, None

    card_name = card.get("name", "")
    try:
        scryfall_card = ScryfallCard.from_scryfall_card(card)
        scryfall_card.save()
        return True, False, None
    except Exception as e:
        print(f"Unable to insert {card_name} due to exception: {e}")
        return False, False, card


@dataclass
class ProcessingResult:
    """Holds the results of card processing."""

    success_count: int = 0
    filtered_count: int = 0
    failed_cards: List[Dict] = None
    processing_time: float = 0.0  # in seconds

    def __post_init__(self):
        if self.failed_cards is None:
            self.failed_cards = []

    def __str__(self) -> str:
        return (
            f"Processing Results:\n"
            f"Successfully processed: {self.success_count} cards\n"
            f"Filtered: {self.filtered_count} cards\n"
            f"Failed: {len(self.failed_cards)} cards\n"
            f"Processing time: {self.processing_time:.2f} seconds"
        )


class ProcessingStrategy(ABC):
    """Abstract base class for card processing strategies."""

    def __init__(self, batch_size: int = 1000):
        self.batch_size = batch_size

    @abstractmethod
    def process(self, cards: List[Dict]) -> ProcessingResult:
        """Process the cards using the specific strategy."""
        pass


class SequentialStrategy(ProcessingStrategy):
    """Process cards sequentially."""

    def process(self, cards: List[Dict]) -> ProcessingResult:
        start_time = datetime.now()
        result = ProcessingResult()

        with transaction.atomic():
            for card in tqdm(cards, desc="Processing cards sequentially"):
                success, filtered, failed_card = process_card(card)
                if success:
                    result.success_count += 1
                elif filtered:
                    result.filtered_count += 1
                elif failed_card:
                    result.failed_cards.append(failed_card)

        result.processing_time = (datetime.now() - start_time).total_seconds()
        return result


class ParallelStrategy(ProcessingStrategy):
    """Parallel processing strategy."""

    def __init__(self, batch_size: int = 1000, max_workers: Optional[int] = None):
        super().__init__(batch_size)
        self.max_workers = max_workers or mp.cpu_count()

    @staticmethod
    def _process_batch(batch: List[Dict]) -> Tuple[int, int, List[Dict]]:
        """Process a batch of cards in a separate process."""
        connections.close_all()

        success = 0
        filtered = 0
        failed = []

        with transaction.atomic():
            for card in batch:
                card_success, card_filtered, failed_card = process_card(card)
                if card_success:
                    success += 1
                elif card_filtered:
                    filtered += 1
                elif failed_card:
                    failed.append(failed_card)

        return success, filtered, failed

    def _chunk_data(self, data: List[Dict]) -> List[List[Dict]]:
        """Split data into chunks for parallel processing."""
        return [
            data[i : i + self.batch_size] for i in range(0, len(data), self.batch_size)
        ]

    def process(self, cards: List[Dict]) -> ProcessingResult:
        start_time = datetime.now()
        result = ProcessingResult()

        # Split data into batches
        batches = self._chunk_data(cards)
        total_batches = len(batches)

        print(f"Processing {len(cards)} cards in {total_batches} batches...")

        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all batches to the process pool
            future_to_batch = {
                executor.submit(self._process_batch, batch): i
                for i, batch in enumerate(batches)
            }

            # Process completed batches with a progress bar
            with tqdm(total=total_batches, desc="Processing batches") as pbar:
                for future in as_completed(future_to_batch):
                    try:
                        success, filtered, failed = future.result()
                        result.success_count += success
                        result.filtered_count += filtered
                        result.failed_cards.extend(failed)
                    except Exception as e:
                        batch_num = future_to_batch[future]
                        print(f"Batch {batch_num} failed with exception: {e}")
                    pbar.update(1)

        result.processing_time = (datetime.now() - start_time).total_seconds()
        return result


class ScryfallExporter:
    """Service class for persisting Scryfall data to the database."""

    def __init__(self):
        if os.getenv("PARALLEL_PROCESSING_ENABLED") == "true":
            self.with_parallel_strategy()
        else:
            self.with_sequential_strategy()

    def process_cards(self, cards: List[Dict]) -> ProcessingResult:
        """Process cards using the specified strategy."""
        print("Clearing scryfall_card database...")
        ScryfallCard.objects.all().delete()
        return self.strategy.process(cards)

    def with_sequential_strategy(self) -> None:
        self.strategy = SequentialStrategy()

    def with_parallel_strategy(self) -> None:
        self.strategy = ParallelStrategy()
