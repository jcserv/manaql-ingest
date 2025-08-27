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

    oracle_text = models.TextField(max_length=1024, null=True, blank=True)
    keywords = ArrayField(models.CharField(max_length=127), null=True, blank=True)
    cmc = models.FloatField(null=True, blank=True)
    mana_cost = models.CharField(max_length=127, null=True, blank=True)
    colors = ArrayField(models.CharField(max_length=1), null=True, blank=True)
    color_identity = ArrayField(models.CharField(max_length=1), null=True, blank=True)
    power = models.CharField(max_length=15, null=True, blank=True)
    toughness = models.CharField(max_length=15, null=True, blank=True)
    games = ArrayField(models.CharField(max_length=7), null=True, blank=True)
    legalities = models.JSONField(null=True, blank=True)
    reserved = models.BooleanField(default=False)
    game_changer = models.BooleanField(default=False)

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
            oracle_text=scryfall_card.get("oracle_text", None),
            keywords=scryfall_card.get("keywords", []),
            cmc=scryfall_card.get("cmc", None),
            mana_cost=scryfall_card.get("mana_cost", None),
            colors=scryfall_card.get("colors", []),
            color_identity=scryfall_card.get("color_identity", []),
            power=scryfall_card.get("power", None),
            toughness=scryfall_card.get("toughness", None),
            games=scryfall_card.get("games", []),
            legalities=scryfall_card.get("legalities", {}),
            reserved=scryfall_card.get("reserved", False),
            game_changer=scryfall_card.get("game_changer", False),
            prices=scryfall_card.get("prices", None),
            image_uris=scryfall_card.get("image_uris", None),
            card_faces=scryfall_card.get("card_faces", None),
        )

    class Meta:
        db_table = "scryfall_card"
