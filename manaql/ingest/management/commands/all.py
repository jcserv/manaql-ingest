from datetime import datetime

from database.models.run_log import Command as MQLCommand
from database.models.run_log import RunLog
from database.models.card import Card
from django.core.management.base import BaseCommand
from services.card_processor import CardProcessor
from services.scryfall import ScryfallService
from services.scryfall_exporter import ScryfallExporter
from services.embedding_service import EmbeddingService


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
            command=MQLCommand.Process, message="Starting embedding generation..."
        )
        embedding_service = EmbeddingService()
        cards_without_embeddings = Card.objects.filter(embedding__isnull=True)
        total_cards = cards_without_embeddings.count()

        if total_cards > 0:
            self.stdout.write(f"Generating embeddings for {total_cards} cards...")
            processed_cards = 0
            failed_cards = 0

            batch_size = 50
            for i in range(0, total_cards, batch_size):
                batch = cards_without_embeddings[i : i + batch_size]
                for card in batch:
                    try:
                        embedding_service.update_card_embedding(card)
                        processed_cards += 1
                    except Exception as e:
                        failed_cards += 1
                        self.stdout.write(
                            f"Failed to generate embedding for {card.name}: {str(e)}"
                        )

                self.stdout.write(
                    f"Processed {min(i + batch_size, total_cards)}/{total_cards} cards"
                )

                if i + batch_size < total_cards:
                    import time

                    time.sleep(1)

            embedding_result = f"Embedding generation complete. Processed: {processed_cards}, Failed: {failed_cards}"
        else:
            embedding_result = "No cards need embedding generation"

        RunLog.objects.create(
            command=MQLCommand.Process,
            message=f"Embedding complete.\n{embedding_result}",
        )

        RunLog.objects.create(
            command=MQLCommand.Process, message=f"Processing complete.\n{result}"
        )

        end_time = datetime.now()
        duration = end_time - start_time

        RunLog.objects.create(
            command=MQLCommand.All,
            message=f"Command finished.\nDuration: {duration}",
        )
