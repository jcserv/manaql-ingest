import gzip
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Iterator
from urllib.parse import urlparse

import ijson
import requests
from tqdm import tqdm


class ScryfallService:
    """Service for interacting with Scryfall API with memory-efficient streaming support."""

    BULK_DATA_URL = "https://api.scryfall.com/bulk-data"

    def __init__(self, app_name: str, app_version: str):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": f"{app_name}/{app_version}",
            }
        )

    def _get_bulk_data_url(self) -> tuple[str, int]:
        """Get the download URL and size for the latest bulk data."""
        response = self.session.get(self.BULK_DATA_URL)
        response.raise_for_status()

        for item in response.json()["data"]:
            if item["type"] == "default_cards":
                return item["download_uri"], item["size"]

        raise ValueError("Could not find default cards bulk data")

    def _download_file(self, url: str, local_path: Path, expected_size: int) -> None:
        """Download a file in chunks while showing progress."""
        response = self.session.get(url, stream=True)
        response.raise_for_status()

        print(
            f"Downloading Scryfall bulk data ({expected_size / (1024*1024):.1f} MB)..."
        )

        with tqdm(total=expected_size, unit="B", unit_scale=True) as pbar:
            with open(local_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))

    def _create_card_iterator(self, file_path: Path) -> Iterator[Dict]:
        """Create an iterator over card objects from a file."""
        print(f"Opening file for parsing: {file_path}")

        def generate_cards():
            if file_path.name.endswith(".gz"):
                file_obj = gzip.open(file_path, "rb")
            else:
                file_obj = open(file_path, "rb")

            try:
                cards = ijson.items(file_obj, "item")
                count = 0
                for card in cards:
                    count += 1
                    if count % 1000 == 0:
                        print(f"Parsed {count} cards...")
                    yield card
            finally:
                file_obj.close()

        return generate_cards()

    @contextmanager
    def stream_all_cards(self) -> Iterator[Dict]:
        """Stream and parse Scryfall bulk data with minimal memory usage."""
        temp_dir = tempfile.TemporaryDirectory()
        try:
            download_url, expected_size = self._get_bulk_data_url()

            filename = os.path.basename(urlparse(download_url).path)
            local_path = Path(temp_dir.name) / filename

            self._download_file(download_url, local_path, expected_size)

            yield self._create_card_iterator(local_path)

        finally:
            temp_dir.cleanup()

    def download_all_cards(self) -> list:
        """Legacy method that downloads all cards into memory."""
        cards = []
        with self.stream_all_cards() as card_stream:
            for card in card_stream:
                cards.append(card)
        return cards
