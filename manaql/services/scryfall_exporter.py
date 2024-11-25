from typing import Dict, List

from database.models.scryfall_card import ScryfallCard


class ScryfallExporterService:
    """Service class for persisting Scryfall data to the database."""

    def process_cards(self, scryfall_cards: List[Dict]) -> None:
        print("Clearing scryfall_card database...")
        ScryfallCard.objects.all().delete()

        success = 0
        failed: List[str] = []

        for card in scryfall_cards:
            try:
                scryfall_card = ScryfallCard.from_scryfall_card(card)
                scryfall_card.save()
                success += 1
            except Exception as e:
                print(
                    f"Unable to insert {card.name} as scryfall_card due to exception: {e}"
                )
                failed.append(card)
                continue

        print(f"Successfully inserted {success} cards into the database")
        if failed:
            print(f"Failed to insert {len(failed)} cards into the database")
            print(failed)
