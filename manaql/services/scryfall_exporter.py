from typing import Dict, List

from services.export_strategy import ProcessingResult, ProcessingStrategy


class ScryfallExporter:
    """Service class for persisting Scryfall data to the database."""

    def process_cards(
        self, cards: List[Dict], strategy: ProcessingStrategy
    ) -> ProcessingResult:
        """Process cards using the specified strategy."""
        return strategy.process(cards)
