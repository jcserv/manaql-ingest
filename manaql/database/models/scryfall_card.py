from common.scryfall import SFCard
from django.contrib.postgres.fields import ArrayField
from django.db import models


class SFCard(models.Model):
    name = models.CharField(max_length=255, null=True)
    set_code = models.CharField(max_length=7, null=True)
    set_name = models.CharField(max_length=255, null=True)
    collector_number = models.CharField(max_length=7, null=True)
    type_line = models.CharField(max_length=255, null=True, blank=True)
    finishes = ArrayField(models.CharField(max_length=20), default=list)

    prices = models.JSONField(default=dict, null=True)
    image_uris = models.JSONField(null=True)
    card_faces = models.JSONField(null=True)

    @staticmethod
    def from_scryfall_card(scryfall_card: SFCard):
        return SFCard(
            **scryfall_card.dict(),
        )

    class Meta:
        db_table = "scryfall_card"
