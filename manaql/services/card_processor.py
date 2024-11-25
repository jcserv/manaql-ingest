from typing import Any, Dict, List

from common.card_type import get_main_type
from database.models.card import Card
from database.models.printing import Printing
from django.db import transaction


class CardProcessor:
    """Service class for processing card data into database records."""

    @staticmethod
    def get_image_uris(card_data: Dict[str, Any]) -> tuple[str | None, str | None]:
        """Extract normal and back image URIs from card data."""
        image_uri = None
        back_image_uri = None

        if "image_uris" in card_data:
            image_uri = card_data["image_uris"].get("normal")
        elif "card_faces" in card_data and len(card_data["card_faces"]) > 0:
            if "image_uris" in card_data["card_faces"][0]:
                image_uri = card_data["card_faces"][0]["image_uris"].get("normal")
            if (
                len(card_data["card_faces"]) > 1
                and "image_uris" in card_data["card_faces"][1]
            ):
                back_image_uri = card_data["card_faces"][1]["image_uris"].get("normal")

        return image_uri, back_image_uri

    def process_cards(self, cards_data: List[Dict[str, Any]], stdout):
        """Process card data and save to database."""
        cards_created = 0
        printings_created = 0

        with transaction.atomic():
            stdout.write("Clearing existing data...")
            Printing.objects.all().delete()
            Card.objects.all().delete()

            stdout.write("Processing cards...")
            cards_by_name = {}

            for card_data in cards_data:
                card_name = card_data["name"]

                # Skip if we've already processed this card
                if card_name in cards_by_name:
                    card = cards_by_name[card_name]
                else:
                    card = Card.objects.create(
                        name=card_name,
                        main_type=get_main_type(card_data.get("type_line", "")),
                    )
                    cards_by_name[card_name] = card
                    cards_created += 1

                image_uri, back_image_uri = self.get_image_uris(card_data)
                if image_uri:  # Only create printing if we have an image
                    Printing.objects.create(
                        card=card,
                        set=card_data["set"],
                        set_name=card_data["set_name"],
                        collector_number=card_data["collector_number"],
                        image_uri=image_uri,
                        back_image_uri=back_image_uri,
                        finishes=card_data.get("finishes", []),
                        price_usd=card_data["prices"].get("usd"),
                        price_usd_foil=card_data["prices"].get("usd_foil"),
                        price_usd_etched=card_data["prices"].get("usd_etched"),
                        price_eur=card_data["prices"].get("eur"),
                        price_eur_foil=card_data["prices"].get("eur_foil"),
                        price_eur_etched=None,  # Not provided by Scryfall
                    )
                    printings_created += 1

                # Progress update every 1000 cards
                if (cards_created + printings_created) % 1000 == 0:
                    stdout.write(
                        f"Processed {cards_created} cards and {printings_created} printings..."
                    )

        return cards_created, printings_created
