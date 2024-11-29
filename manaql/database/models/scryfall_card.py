from typing import Dict

from django.contrib.postgres.fields import ArrayField
from django.db import models


class ScryfallCard(models.Model):
    name = models.CharField(max_length=255, null=True)
    lang = models.CharField(max_length=5, null=True)
    set_code = models.CharField(max_length=7, null=True)
    set_name = models.CharField(max_length=255, null=True)
    collector_number = models.CharField(max_length=31, null=True)
    type_line = models.CharField(max_length=255, null=True, blank=True)
    finishes = ArrayField(models.CharField(max_length=20), default=list)
    promo_types = ArrayField(models.CharField(max_length=20), default=list)

    prices = models.JSONField(null=True)
    image_uris = models.JSONField(null=True)
    card_faces = models.JSONField(null=True)

    @staticmethod
    def from_scryfall_card(scryfall_card: Dict):
        return ScryfallCard(
            name=scryfall_card.get("name", None),
            lang=scryfall_card.get("lang", None),
            set_code=scryfall_card.get("set", None),
            set_name=scryfall_card.get("set_name", None),
            collector_number=scryfall_card.get("collector_number", None),
            type_line=scryfall_card.get("type_line", None),
            finishes=scryfall_card.get("finishes", []),
            promo_types=scryfall_card.get("promo_types", []),
            prices=scryfall_card.get("prices", None),
            image_uris=scryfall_card.get("image_uris", None),
            card_faces=scryfall_card.get("card_faces", None),
        )

    class Meta:
        db_table = "scryfall_card"
