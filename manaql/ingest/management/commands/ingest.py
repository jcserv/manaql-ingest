import json
from datetime import datetime

from common.utils import get_artifact_file_path
from django.core.management.base import BaseCommand
from services.scryfall import ScryfallService
from services.scryfall_exporter import ScryfallExporter


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
        print("Starting card data ingest...")

        if options["file_path"]:
            file_path = get_artifact_file_path(options["file_path"])
            print(f"Loading data from {file_path}...")
            with open(file_path, "r", encoding="utf-8") as f:
                cards_data = json.load(f)
        else:
            print("Downloading fresh data from Scryfall...")
            client = ScryfallService("manaql-ingest", "0.1.0")
            cards_data = client.download_all_cards()

        print("Processing card data...")

        exporter = ScryfallExporter()
        result = exporter.process_cards(cards_data)
        print(result)

        end_time = datetime.now()
        duration = end_time - start_time

        self.stdout.write(self.style.SUCCESS(f"\nIngestion completed in {duration}"))
