from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand
from services.scryfall import ScryfallService

ARTIFACTS_DIR = Path("artifacts")


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
            action="store_true",
            help="Fetch the bulk data URL without writing an artifact",
        )

    def handle(self, *args, **options):
        start_time = datetime.now()

        client = ScryfallService("manaql-ingest", "0.1.0")

        if options["dry_run"]:
            url, size = client._get_bulk_data_url()
            self.stdout.write(
                self.style.SUCCESS(f"Dry run: would download {url} ({size} bytes)")
            )
            return

        destination = ARTIFACTS_DIR / options["file_name"]
        saved_path = client.download_bulk_data_to_file(destination)

        duration = datetime.now() - start_time

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully downloaded Scryfall data to {saved_path}\n"
                f"Download completed in {duration}"
            )
        )
