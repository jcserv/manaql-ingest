from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand
from services.scryfall import ScryfallService


class Command(BaseCommand):
    help = "Downloads Scryfall bulk data to a JSON file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file-name",
            type=str,
            help="Name of the file to save (will be saved under artifacts/)",
            default="scryfall_data.json",
        )

        parser.add_argument(
            "--dry-run",
            type=bool,
            help="Whether to run the command in dry-run mode (no data will be saved)",
            default=False,
        )

    def handle(self, *args, **options):
        start_time = datetime.now()
        self.stdout.write("Starting Scryfall data download...")

        artifacts_dir = Path("artifacts")
        artifacts_dir.mkdir(exist_ok=True)

        file_path = artifacts_dir / options["file_name"]

        client = ScryfallService("manaql-ingest", "0.1.0")
        client.download_all_cards(save_path=str(file_path))

        end_time = datetime.now()
        duration = end_time - start_time

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully downloaded Scryfall data to {file_path}\n"
                f"Download completed in {duration}"
            )
        )
