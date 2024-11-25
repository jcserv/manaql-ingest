from typing import Dict, List

from common.scryfall import SFCard
from database.models.card import Card
from database.models.printing import Printing
from psycopg2 import IntegrityError


class CardProcessor:
    """Service class for processing card data into database records."""

    def process_cards(self, scryfall_cards: List[SFCard]) -> tuple[int, int]:
        """Process card data and save to database.

        Returns:
            tuple[int, int]: Count of (cards_created, printings_created)
        """
        cards_created = 0
        printings_created = 0
        seen_cards = set()  # Track which cards we've already seen

        print("Clearing existing data...")
        Printing.objects.all().delete()
        Card.objects.all().delete()

        print("Processing cards...")
        cards_by_name: Dict[str, Card] = {}

        # First pass: Create all unique cards
        for scryfall_card in scryfall_cards:
            card_name = scryfall_card.name

            if card_name not in seen_cards:
                try:
                    card = Card.from_scryfall_card(scryfall_card)
                    card.save()
                except IntegrityError as e:
                    print(f"Unable to insert {card_name} as card due to exception: {e}")
                    continue

                cards_by_name[card_name] = card
                cards_created += 1
                seen_cards.add(card_name)

                if cards_created % 1000 == 0:
                    print(f"Created {cards_created} unique cards...")

        # Second pass: Create all printings
        for scryfall_card in scryfall_cards:
            card_name = scryfall_card.name
            card = cards_by_name[card_name]  # We know this exists from first pass

            try:
                p = Printing.from_scryfall_card(card, scryfall_card)
                p.save()
            except Exception as e:
                print(f"Unable to insert {card_name} as printing due to exception: {e}")
                continue

            printings_created += 1

            if printings_created % 1000 == 0:
                print(f"Created {printings_created} printings...")

        return cards_created, printings_created
