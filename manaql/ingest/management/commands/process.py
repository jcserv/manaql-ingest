from datetime import datetime

from django.core.management.base import BaseCommand
from services.card_processor import CardProcessor


class Command(BaseCommand):
    help = "Processes Scryfall card data into our format"

    def handle(self, *args, **options):
        start_time = datetime.now()
        print("Starting card data processing...")

        processor = CardProcessor()
        result = processor.process_cards()
        print(result)

        end_time = datetime.now()
        duration = end_time - start_time

        self.stdout.write(self.style.SUCCESS(f"\nProcessing completed in {duration}"))
