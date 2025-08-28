from datetime import datetime
import time
from django.core.management.base import BaseCommand
from services.embedding_service import EmbeddingService
from database.models.card import Card
from database.models.run_log import Command as MQLCommand
from database.models.run_log import RunLog


class Command(BaseCommand):
    help = "Generate embeddings for cards in the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch-size",
            type=int,
            default=50,
            help="Number of cards to process in each batch (default: 50)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be processed without actually generating embeddings",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Regenerate embeddings for cards that already have them",
        )
        parser.add_argument(
            "--limit",
            type=int,
            help="Limit the number of cards to process (useful for testing)",
        )

    def handle(self, *args, **options):
        start_time = datetime.now()
        batch_size = options["batch_size"]
        dry_run = options["dry_run"]
        force = options["force"]
        limit = options["limit"]

        self.stdout.write("Starting embedding generation...")

        if force:
            cards_to_process = Card.objects.all()
            self.stdout.write(
                f"Force mode: will process all {cards_to_process.count()} cards"
            )
        else:
            cards_to_process = Card.objects.filter(embedding__isnull=True)
            self.stdout.write(
                f"Found {cards_to_process.count()} cards without embeddings"
            )

        if limit:
            cards_to_process = cards_to_process[:limit]
            self.stdout.write(f"Limited to {limit} cards for processing")

        if dry_run:
            self.stdout.write(
                f"DRY RUN: Would process {cards_to_process.count()} cards"
            )
            return

        if not cards_to_process.exists():
            self.stdout.write(self.style.SUCCESS("No cards need embedding generation!"))
            return

        RunLog.objects.create(
            command=MQLCommand.Process,
            message=f"Starting embedding generation for {cards_to_process.count()} cards",
        )

        embedding_service = EmbeddingService()
        total_cards = cards_to_process.count()
        processed_cards = 0
        failed_cards = 0

        for i in range(0, total_cards, batch_size):
            batch_start_time = time.time()
            batch = cards_to_process[i : i + batch_size]

            self.stdout.write(
                f"Processing batch {i//batch_size + 1}/{(total_cards + batch_size - 1)//batch_size} "
                f"({i+1}-{min(i+batch_size, total_cards)} of {total_cards})"
            )

            for card in batch:
                try:
                    if not dry_run:
                        embedding_service.update_card_embedding(card)
                    processed_cards += 1
                except Exception as e:
                    failed_cards += 1
                    self.stdout.write(
                        self.style.ERROR(
                            f"Failed to generate embedding for {card.name}: {str(e)}"
                        )
                    )

            batch_duration = time.time() - batch_start_time
            self.stdout.write(f"  Batch completed in {batch_duration:.2f}s")

        end_time = datetime.now()
        duration = end_time - start_time

        summary = (
            f"Embedding generation completed in {duration}\n"
            f"Total cards: {total_cards}\n"
            f"Successfully processed: {processed_cards}\n"
            f"Failed: {failed_cards}"
        )

        self.stdout.write(self.style.SUCCESS(summary))

        RunLog.objects.create(
            command=MQLCommand.Process,
            message=f"Embedding generation complete.\n{summary}",
        )
