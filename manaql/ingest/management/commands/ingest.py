import json
from datetime import datetime
from pathlib import Path

from common.scryfall import ScryfallCard
from django.core.management.base import BaseCommand, CommandError
from services.card_processor import CardProcessor
from services.scryfall import ScryfallService


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
            artifacts_dir = Path(__file__).resolve().parent.parent.parent / "artifacts"
            file_path = artifacts_dir / options["file_path"]

            if not artifacts_dir.exists():
                raise CommandError(
                    f"Artifacts directory not found at {artifacts_dir}. "
                    "Please create this directory and ensure your data file is placed there."
                )

            if not file_path.exists():
                raise CommandError(
                    f"File not found: {file_path}\n"
                    f"Please ensure your file exists in the artifacts directory: {artifacts_dir}"
                )

            self.stdout.write(f"Loading data from {file_path}...")
            with open(file_path, "r", encoding="utf-8") as f:
                cards_data = json.load(f)
                cards_data = ScryfallCard.from_list(cards_data)
        else:
            self.stdout.write("Downloading fresh data from Scryfall...")
            client = ScryfallService("manaql-ingest", "0.1.0")
            cards_data = client.download_all_cards()

        self.stdout.write("Processing card data...")
        processor = CardProcessor()
        cards_created, printings_created = processor.process_cards(cards_data)

        end_time = datetime.now()
        duration = end_time - start_time

        self.stdout.write(self.style.SUCCESS(f"\nIngestion completed in {duration}"))
