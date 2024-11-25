from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from pathlib import Path
import json

from services.scryfall import ScryfallService
from services.card_processor import CardProcessor


class Command(BaseCommand):
    help = "Ingests Scryfall card data into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file-path",
            type=str,
            help="Path to JSON file containing Scryfall data (if not provided, will download fresh data)",
        )

    def handle(self, *args, **options):
        start_time = datetime.now()
        self.stdout.write("Starting card data ingest...")

        if options["file_path"]:
            file_path = Path(options["file_path"])
            if not file_path.exists():
                raise CommandError(f"File not found: {file_path}")

            self.stdout.write(f"Loading data from {file_path}...")
            with open(file_path, "r", encoding="utf-8") as f:
                cards_data = json.load(f)
        else:
            self.stdout.write("Downloading fresh data from Scryfall...")
            client = ScryfallService("manaql-ingest", "0.1.0")
            cards_data = client.download_all_cards()

        self.stdout.write("Processing card data...")
        processor = CardProcessor()
        cards_created, printings_created = processor.process_cards(
            cards_data, self.stdout
        )

        end_time = datetime.now()
        duration = end_time - start_time

        self.stdout.write(self.style.SUCCESS(f"\nIngestion completed in {duration}"))
