import time
import json
from typing import Optional, Dict, Any, List
import requests

from common.bulk_data import BulkData


class ScryfallClient:
    BASE_URL = "https://api.scryfall.com"

    def __init__(self, app_name: str, version: str):
        """
        Initialize the Scryfall client.

        Args:
            app_name: The name of your application
            version: The version of your application
        """
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": f"{app_name}/{version}", "Accept": "application/json"}
        )
        self.last_request_time = 0

    def _enforce_rate_limit(self):
        """Enforce rate limiting by adding delay between requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time

        if time_since_last < 0.1:
            sleep_time = 0.1 - time_since_last
            time.sleep(sleep_time)

        self.last_request_time = time.time()

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make a rate-limited request to the Scryfall API.

        Args:
            method: HTTP method to use
            endpoint: API endpoint to call
            **kwargs: Additional arguments to pass to requests

        Returns:
            Parsed JSON response
        """
        self._enforce_rate_limit()

        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        response = self.session.request(method, url, **kwargs)

        if response.status_code == 429:
            raise Exception("Rate limit exceeded. Please reduce request frequency.")

        response.raise_for_status()
        return response.json()

    def get_bulk_data(self) -> List[BulkData]:
        """
        Get the list of all available bulk data downloads.

        Returns:
            List of BulkData objects
        """
        response = self._make_request("GET", "/bulk-data")
        return [
            BulkData(
                id=item["id"],
                type=item["type"],
                updated_at=item["updated_at"],
                uri=item["uri"],
                name=item["name"],
                description=item["description"],
                size=item["size"],
                download_uri=item["download_uri"],
                content_type=item["content_type"],
                content_encoding=item["content_encoding"],
            )
            for item in response["data"]
        ]

    def download_all_cards(
        self, save_path: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Download and optionally save the all cards bulk data.

        Args:
            save_path: Optional path to save the JSON data to a file

        Returns:
            List of card objects from the bulk data
        """
        # Get bulk data information
        bulk_data = self.get_bulk_data()
        all_cards_data = next(item for item in bulk_data if item.type == "all_cards")

        # Download the data
        print(f"Downloading {all_cards_data.size / 1024 / 1024:.1f} MB of card data...")
        response = requests.get(all_cards_data.download_uri)
        response.raise_for_status()

        cards = response.json()

        # Optionally save to file
        if save_path:
            print(f"Saving data to {save_path}...")
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(cards, f, indent=2)

        return cards
