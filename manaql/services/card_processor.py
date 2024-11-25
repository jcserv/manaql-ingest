from typing import List

from common.card_type import get_main_type
from common.finish import get_finishes
from common.scryfall import ScryfallCard
from database.models.card import Card
from database.models.printing import Printing
from django.db import transaction


class CardProcessor:
    """Service class for processing card data into database records."""

    @staticmethod
    def get_image_uris(scryfall_card: ScryfallCard) -> tuple[str | None, str | None]:
        """Extract normal and back image URIs from card data."""
        image_uri = None
        back_image_uri = None

        if scryfall_card.image_uris:
            image_uri = scryfall_card.image_uris.normal
        elif scryfall_card.card_faces and len(scryfall_card.card_faces) > 0:
            if scryfall_card.card_faces[0].image_uris:
                image_uri = scryfall_card.card_faces[0].image_uris.normal
            if (
                len(scryfall_card.card_faces) > 1
                and scryfall_card.card_faces[1].image_uris
            ):
                back_image_uri = scryfall_card.card_faces[1].image_uris.normal
        return image_uri, back_image_uri

    def process_cards(self, scryfall_cards: List[ScryfallCard]) -> tuple[int, int]:
        """Process card data and save to database.

        Returns:
            tuple[int, int]: Count of (cards_created, printings_created)
        """
        cards_created = 0
        printings_created = 0
        seen_cards = set()  # Track which cards we've already seen

        with transaction.atomic():
            print("Clearing existing data...")
            Printing.objects.all().delete()
            Card.objects.all().delete()

            print("Processing cards...")
            cards_by_name = {}

            # First pass: Create all unique cards
            for scryfall_card in scryfall_cards:
                card_name = scryfall_card.name

                if card_name not in seen_cards:
                    card = Card.objects.create(
                        name=card_name,
                        main_type=get_main_type(scryfall_card.type_line),
                    )
                    cards_by_name[card_name] = card
                    cards_created += 1
                    seen_cards.add(card_name)

                    if cards_created % 1000 == 0:
                        print(f"Created {cards_created} unique cards...")

            # Second pass: Create all printings
            for scryfall_card in scryfall_cards:
                card_name = scryfall_card.name
                card = cards_by_name[card_name]  # We know this exists from first pass

                image_uri, back_image_uri = self.get_image_uris(scryfall_card)
                if image_uri:  # Only create printing if we have an image
                    Printing.objects.create(
                        card_id=card,
                        set_code=scryfall_card.set,
                        set_name=scryfall_card.set_name,
                        collector_number=scryfall_card.collector_number,
                        image_uri=image_uri,
                        back_image_uri=back_image_uri,
                        finishes=get_finishes(scryfall_card.finishes),
                        price_usd=scryfall_card.prices.usd,
                        price_usd_foil=scryfall_card.prices.usd_foil,
                        price_usd_etched=scryfall_card.prices.usd_etched,
                        price_eur=scryfall_card.prices.eur,
                        price_eur_foil=scryfall_card.prices.eur_foil,
                        price_eur_etched=None,  # TODO:Not provided by Scryfall, can guesstimate?
                    )
                    printings_created += 1

                    if printings_created % 1000 == 0:
                        print(f"Created {cards_created} cards...")

        return cards_created, printings_created
