from django.core.management.base import BaseCommand
from django.db import transaction
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path
import json

from database.models.card import Card
from database.models.printing import Printing
from services.scryfall.client import ScryfallClient


class Command(BaseCommand):
    help = "Downloads and processes Scryfall bulk data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--save-json",
            action="store_true",
            help="Save the downloaded JSON to a file",
        )
        parser.add_argument(
            "--json-path",
            type=str,
            help="Path to save or load JSON data",
            default="scryfall_data.json",
        )

    def _map_card_type(self, card_data: Dict[str, Any]) -> str:
        """Map Scryfall card type to our enum values."""
        type_line = card_data.get("type_line", "").lower()

        # Map card types based on type_line
        if "creature" in type_line:
            return "Creature"
        elif "planeswalker" in type_line:
            return "Planeswalker"
        elif "instant" in type_line:
            return "Instant"
        elif "sorcery" in type_line:
            return "Sorcery"
        elif "artifact" in type_line:
            return "Artifact"
        elif "enchantment" in type_line:
            return "Enchantment"
        elif "land" in type_line:
            return "Land"
        elif "tribal" in type_line:
            return "Kindred"
        elif "battle" in type_line:
            return "Battle"
        elif "conspiracy" in type_line:
            return "Conspiracy"
        elif "dungeon" in type_line:
            return "Dungeon"
        elif "phenomenon" in type_line:
            return "Phenomenon"
        elif "plane" in type_line:
            return "Plane"
        elif "scheme" in type_line:
            return "Scheme"
        elif "vanguard" in type_line:
            return "Vanguard"

        # Default to the most common type if we can't determine it
        return "Creature"

    def _process_cards(self, cards_data: List[Dict[str, Any]]):
        """Process card data and save to database."""
        cards_created = 0
        printings_created = 0

        with transaction.atomic():
            # First, clear existing data
            self.stdout.write("Clearing existing data...")
            Printing.objects.all().delete()
            Card.objects.all().delete()

            # Process each card
            self.stdout.write("Processing cards...")
            cards_by_name = {}

            for card_data in cards_data:
                card_name = card_data["name"]

                # Skip if we've already processed this card
                if card_name in cards_by_name:
                    card = cards_by_name[card_name]
                else:
                    # Create new card
                    card = Card.objects.create(
                        name=card_name, main_type=self._map_card_type(card_data)
                    )
                    cards_by_name[card_name] = card
                    cards_created += 1

                # Get image URIs
                image_uri = None
                back_image_uri = None

                if "image_uris" in card_data:
                    image_uri = card_data["image_uris"].get("normal")
                elif "card_faces" in card_data and len(card_data["card_faces"]) > 0:
                    if "image_uris" in card_data["card_faces"][0]:
                        image_uri = card_data["card_faces"][0]["image_uris"].get(
                            "normal"
                        )
                    if (
                        len(card_data["card_faces"]) > 1
                        and "image_uris" in card_data["card_faces"][1]
                    ):
                        back_image_uri = card_data["card_faces"][1]["image_uris"].get(
                            "normal"
                        )

                # Create printing
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
                    self.stdout.write(
                        f"Processed {cards_created} cards and {printings_created} printings..."
                    )

        return cards_created, printings_created

    def handle(self, *args, **options):
        start_time = datetime.now()
        self.stdout.write("Starting Scryfall data import...")

        # Initialize client
        client = ScryfallClient("manaql-ingest", "0.1.0")

        json_path = Path(options["json_path"])

        # Download or load data
        if json_path.exists() and not options["save_json"]:
            self.stdout.write(f"Loading data from {json_path}...")
            with open(json_path, "r", encoding="utf-8") as f:
                cards_data = json.load(f)
        else:
            self.stdout.write("Downloading data from Scryfall...")
            cards_data = client.download_all_cards(
                save_path=str(json_path) if options["save_json"] else None
            )

        # Process the data
        self.stdout.write("Processing card data...")
        cards_created, printings_created = self._process_cards(cards_data)

        # Report results
        end_time = datetime.now()
        duration = end_time - start_time

        self.stdout.write(
            self.style.SUCCESS(
                f"\nImport completed in {duration}:\n"
                f"- Created {cards_created} cards\n"
                f"- Created {printings_created} printings"
            )
        )
