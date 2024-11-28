from datetime import datetime

from database.models.run_log import Command as MQLCommand
from database.models.run_log import RunLog
from django.core.management.base import BaseCommand
from services.card_processor import CardProcessor
from services.scryfall import ScryfallService
from services.scryfall_exporter import ScryfallExporter


class Command(BaseCommand):
    help = "Do all the things."

    def handle(self, *args, **options):
        start_time = datetime.now()

        RunLog.objects.create(command=MQLCommand.All, message="Starting command...")
        client = ScryfallService("manaql-ingest", "0.1.0")
        with client.stream_all_cards() as cards_iterator:
            RunLog.objects.create(
                command=MQLCommand.Download, message="Download in progress..."
            )
            exporter = ScryfallExporter()
            result = exporter.process_cards(cards_iterator)
            RunLog.objects.create(
                command=MQLCommand.Ingest, message=f"Ingestion complete.\n{result}"
            )

        processor = CardProcessor()
        result = processor.process_cards()
        RunLog.objects.create(
            command=MQLCommand.Process, message=f"Processing complete.\n{result}"
        )

        end_time = datetime.now()
        duration = end_time - start_time

        RunLog.objects.create(
            command=MQLCommand.All,
            message=f"Command finished.\nDuration: {duration}",
        )
