import json
from datetime import datetime
from typing import Dict, List

from common.utils import get_artifact_file_path
from database.models.scryfall_card import ScryfallCard


class ScryfallExporter:
    """Service class for persisting Scryfall data to the database."""

    def filter(self, scryfall_card: Dict) -> bool:
        if scryfall_card.get("lang", None) != "en":
            return True
        if scryfall_card.get("layout", "") != "normal":
            return True
        if "paper" not in scryfall_card.get("games", []):
            return True
        return False

    def process_cards(self, scryfall_cards: List[Dict]) -> None:
        print("Clearing scryfall_card database...")
        ScryfallCard.objects.all().delete()

        success = 0
        filtered = 0
        failed: List[str] = []

        for card in scryfall_cards:
            if self.filter(card):
                filtered += 1
                continue

            card_name = card.get("name", "")
            try:
                scryfall_card = ScryfallCard.from_scryfall_card(card)
                scryfall_card.save()
                success += 1
            except Exception as e:
                print(
                    f"Unable to insert {card_name} as scryfall_card due to exception: {e}"
                )
                failed.append(card)
                continue

        print(f"Successfully inserted {success} cards into the database")
        print(f"Filtered out {filtered} cards")

        if failed:
            print(f"Failed to insert {len(failed)} cards into the database")
            file_name = f"failed_scryfall_cards_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
            print(f"Failed cards saved to artifacts/${file_name}.json")
            file_path = get_artifact_file_path(file_name)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(failed, f, indent=2)
