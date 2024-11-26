from datetime import datetime

from django.core.management.base import BaseCommand
from services.card_processor import CardProcessor
from services.scryfall import ScryfallService
from services.scryfall_exporter import ScryfallExporter


class Command(BaseCommand):
    help = "Do all the things."

    def handle(self, *args, **options):
        start_time = datetime.now()

        print("Starting Scryfall data download...")
        client = ScryfallService("manaql-ingest", "0.1.0")
        cards_data = client.download_all_cards()

        print("Offloading Scryfall data to database...")
        exporter = ScryfallExporter()
        result = exporter.process_cards(cards_data)
        print(result)

        print("Processing card data...")
        result = CardProcessor().process_cards()
        print(result)

        end_time = datetime.now()
        duration = end_time - start_time
        self.stdout.write(
            self.style.SUCCESS(f"Ingestion complete.\n" f"Duration: {duration}")
        )
