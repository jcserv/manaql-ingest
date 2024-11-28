import gc
import multiprocessing as mp
import os
from abc import ABC, abstractmethod
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Iterator, List, Optional, Tuple

from database.models.scryfall_card import ScryfallCard
from django.db import connections, transaction


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
            card_objects = []
            for card in cards:
                if filterCard(card):
                    result.filtered_count += 1
                    continue
                card_objects.append(ScryfallCard.from_scryfall_card(card))
            ScryfallCard.objects.bulk_create(card_objects)
            result.success_count = len(card_objects)

        result.processing_time = (datetime.now() - start_time).total_seconds()
        return result


class ParallelStrategy(ProcessingStrategy):
    """Memory-optimized parallel processing strategy."""

    def __init__(self, batch_size: int = 1000, max_workers: Optional[int] = None):
        super().__init__(batch_size)
        self.max_workers = min(max_workers or mp.cpu_count(), 4)

    @staticmethod
    def _process_batch(batch: List[Dict]) -> Tuple[int, int, List[Dict]]:
        """Process a batch of cards in a separate process with proper cleanup"""
        connections.close_all()
        success = filtered = 0
        failed = []

        try:
            with transaction.atomic():
                card_objects = []
                for card in batch:
                    if filterCard(card):
                        filtered += 1
                        continue
                    card_objects.append(ScryfallCard.from_scryfall_card(card))

                ScryfallCard.objects.bulk_create(card_objects, batch_size=1000)
                success = len(card_objects)
        finally:
            # Clean up references
            del card_objects
            gc.collect()

        return success, filtered, failed

    def process(self, cards: Iterator[Dict]) -> ProcessingResult:
        start_time = datetime.now()
        result = ProcessingResult()

        # Process cards in batches using a generator approach
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            # Create a queue to store futures
            futures = []
            current_batch = []

            for card in cards:
                current_batch.append(card)

                if len(current_batch) >= self.batch_size:
                    # Submit the batch for processing
                    futures.append(executor.submit(self._process_batch, current_batch))
                    current_batch = []

                    # Process completed futures if we have enough
                    if len(futures) >= self.max_workers * 2:
                        self._process_completed_futures(futures, result)
                        futures = []

            # Process any remaining cards in the last batch
            if current_batch:
                futures.append(executor.submit(self._process_batch, current_batch))

            # Process any remaining futures
            self._process_completed_futures(futures, result)

        result.processing_time = (datetime.now() - start_time).total_seconds()
        return result

    def _process_completed_futures(
        self, futures: List, result: ProcessingResult
    ) -> None:
        """Process completed futures and update results"""
        for future in as_completed(futures):
            try:
                success, filtered, failed = future.result()
                result.success_count += success
                result.filtered_count += filtered
                result.failed_cards.extend(failed)
            except Exception as e:
                print(f"Batch processing failed with exception: {e}")
            finally:
                del future


class ScryfallExporter:
    """Service class for persisting Scryfall data to the database."""

    _db_cleared = False

    def __init__(self):
        if os.getenv("PARALLEL_PROCESSING_ENABLED") == "true":
            self.with_parallel_strategy()
        else:
            self.with_sequential_strategy()

    def process_cards(self, cards: List[Dict]) -> ProcessingResult:
        """Process cards using the specified strategy."""
        self._clear_database_once()
        return self.strategy.process(cards)

    def with_sequential_strategy(self) -> None:
        self.strategy = SequentialStrategy()

    def with_parallel_strategy(self) -> None:
        self.strategy = ParallelStrategy()

    @classmethod
    def _clear_database_once(cls) -> None:
        """Clear the database only on the first execution."""
        if not cls._db_cleared:
            print("Clearing scryfall_card database...")
            ScryfallCard.objects.all().delete()
            cls._db_cleared = True
