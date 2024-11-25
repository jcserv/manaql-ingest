from common.scryfall import ScryfallCard
from django.contrib.postgres.fields import ArrayField
from django.db import models


class FailedCard(models.Model):
    name = models.CharField(max_length=255)
    set_code = models.CharField(max_length=7)
    set_name = models.CharField(max_length=255)
    collector_number = models.CharField(max_length=7)
    type_line = models.CharField(max_length=255, null=True, blank=True)
    finishes = ArrayField(models.CharField(max_length=20), default=list)

    prices = models.JSONField(default=dict)
    image_uris = models.JSONField(null=True)
    card_faces = models.JSONField(null=True)

    @staticmethod
    def from_scryfall_card(scryfall_card: ScryfallCard):
        return FailedCard(
            **scryfall_card.dict(),
        )

    class Meta:
        db_table = "failed_card"
