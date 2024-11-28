import multiprocessing as mp
import os
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Set

from database.models.card import Card
from database.models.printing import Printing
from database.models.scryfall_card import ScryfallCard
from django.db import transaction
from tqdm import tqdm


@dataclass
class ProcessingResult:
    """Holds the results of card and printing processing."""

    cards_created: int = 0
    printings_created: int = 0
    failed_cards: List[str] = None
    failed_printings: List[str] = None
    processing_time: float = 0.0

    def __post_init__(self):
        if self.failed_cards is None:
            self.failed_cards = []
        if self.failed_printings is None:
            self.failed_printings = []

    def __str__(self) -> str:
        return (
            f"Processing Results:\n"
            f"Cards created: {self.cards_created}\n"
            f"Printings created: {self.printings_created}\n"
            f"Failed cards: {len(self.failed_cards)}\n"
            f"Failed printings: {len(self.failed_printings)}\n"
            f"Processing time: {self.processing_time:.2f} seconds"
        )


class ProcessingStrategy(ABC):
    """Abstract base class for card processing strategies."""

    @abstractmethod
    def process(self) -> ProcessingResult:
        """Process the cards using the specific strategy."""
        pass


class SequentialStrategy(ProcessingStrategy):
    """Process cards sequentially."""

    def process(self) -> ProcessingResult:
        start_time = datetime.now()
        result = ProcessingResult()
        processed_names = set()

        print("Processing cards sequentially...")
        scryfall_cards = ScryfallCard.objects.all()

        # First pass: Create all unique cards
        for scryfall_card in scryfall_cards:
            if scryfall_card.name not in processed_names:
                try:
                    card = Card.from_scryfall_card(scryfall_card)
                    card.save()
                    processed_names.add(scryfall_card.name)
                    result.cards_created += 1
                except Exception as e:
                    print(f"Error creating card {scryfall_card.name}: {e}")
                    result.failed_cards.append(scryfall_card.name)
                    continue

        # Pre-fetch all cards for the second pass
        cards_by_name = {card.name: card for card in Card.objects.all()}

        # Second pass: Create all printings
        for scryfall_card in scryfall_cards:
            try:
                card = cards_by_name.get(scryfall_card.name)
                printing = Printing.from_scryfall_card(card.id, scryfall_card)
                printing.save()
                result.printings_created += 1
            except Exception as e:
                print(f"Error creating printing for {scryfall_card.name}: {e}")
                result.failed_printings.append(scryfall_card.name)

        result.processing_time = (datetime.now() - start_time).total_seconds()
        return result


class ParallelStrategy(ProcessingStrategy):
    """Process cards in parallel using thread pools."""

    def __init__(self, batch_size: int = 1000, max_workers: Optional[int] = None):
        self.batch_size = batch_size
        self.max_workers = max_workers or (mp.cpu_count() * 2)

    def _create_cards(self, scryfall_cards: List[ScryfallCard]) -> Set[str]:
        """Create all unique cards and return set of processed names."""
        processed_names = set()

        for scryfall_card in scryfall_cards:
            if scryfall_card.name not in processed_names:
                try:
                    card = Card.from_scryfall_card(scryfall_card)
                    card.save()
                    processed_names.add(scryfall_card.name)
                except Exception as e:
                    print(f"Error creating card {scryfall_card.name}: {e}")

        return processed_names

    def _process_printing_batch(
        self, scryfall_cards: List[ScryfallCard]
    ) -> tuple[List[str], int]:
        """Process a batch of printings."""
        failed_printings = []
        printings_created = 0

        # Pre-fetch cards needed for this batch
        card_names = {sc.name for sc in scryfall_cards}
        cards_by_name = {
            card.name: card for card in Card.objects.filter(name__in=card_names)
        }

        for scryfall_card in scryfall_cards:
            card = cards_by_name.get(scryfall_card.name)
            if not card:
                failed_printings.append(scryfall_card.name)
                continue

            try:
                printing = Printing.from_scryfall_card(card.id, scryfall_card)
                printing.save()
                printings_created += 1
            except Exception as e:
                print(f"Error creating printing for {scryfall_card.name}: {e}")
                failed_printings.append(scryfall_card.name)

        return failed_printings, printings_created

    def process(self) -> ProcessingResult:
        start_time = datetime.now()
        result = ProcessingResult()

        # First, create all cards in a single transaction
        print("Creating all unique cards...")
        scryfall_cards = list(ScryfallCard.objects.all())

        with transaction.atomic():
            processed_names = self._create_cards(scryfall_cards)
            result.cards_created = len(processed_names)

        # Then process printings in parallel batches
        print("Processing printings in parallel...")
        batches = [
            scryfall_cards[i : i + self.batch_size]
            for i in range(0, len(scryfall_cards), self.batch_size)
        ]

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_batch = {
                executor.submit(self._process_printing_batch, batch): batch
                for batch in batches
            }

            with tqdm(total=len(batches), desc="Processing batches") as pbar:
                for future in as_completed(future_to_batch):
                    try:
                        failed_printings, printings_created = future.result()
                        result.printings_created += printings_created
                        result.failed_printings.extend(failed_printings)
                    except Exception as e:
                        print(f"Batch processing failed with error: {e}")
                    pbar.update(1)

        result.processing_time = (datetime.now() - start_time).total_seconds()
        return result


class CardProcessor:
    """Service class for processing card data from ScryfallCard table."""

    def __init__(self):
        if os.getenv("PARALLEL_PROCESSING_ENABLED") == "true":
            self.with_parallel_strategy()
        else:
            self.with_sequential_strategy()

    def process_cards(self) -> ProcessingResult:
        """Process cards using the specified strategy."""
        print("Clearing card/printing databases...")
        with transaction.atomic():
            Printing.objects.all().delete()
            Card.objects.all().delete()

        return self.strategy.process()

    def with_sequential_strategy(self) -> None:
        self.strategy = SequentialStrategy()

    def with_parallel_strategy(self) -> None:
        self.strategy = ParallelStrategy()
