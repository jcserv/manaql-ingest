from django.contrib.postgres.fields import ArrayField
from django.db import models


class ScryfallCard(models.Model):
    name = models.CharField(max_length=255, null=True)
    lang = models.CharField(max_length=5, null=True)
    set_code = models.CharField(max_length=7, null=True)
    set_name = models.CharField(max_length=255, null=True)
    collector_number = models.CharField(max_length=7, null=True)
    type_line = models.CharField(max_length=255, null=True, blank=True)
    finishes = ArrayField(models.CharField(max_length=20), default=list)

    prices = models.JSONField(default=dict, null=True)
    image_uris = models.JSONField(null=True)
    card_faces = models.JSONField(null=True)

    # @staticmethod
    # def from_scryfall_card(scryfall_card: SFCard) -> "ScryfallCard":
    #     return ScryfallCard(
    #         name=scryfall_card.name,
    #         lang=scryfall_card.lang,
    #         set_code=scryfall_card.set,
    #         set_name=scryfall_card.set_name,
    #         collector_number=scryfall_card.collector_number,
    #         type_line=scryfall_card.type_line,
    #         finishes=scryfall_card.finishes,
    #         prices=prices_dict,
    #         image_uris=image_uris_dict,
    #         card_faces=card_faces_dict,
    #     )

    class Meta:
        db_table = "scryfall_card"
