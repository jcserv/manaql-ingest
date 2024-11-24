from django.db import models

from common.card_type import CardType


class Card(models.Model):
    card_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    main_type = models.CharField(max_length=31, null=False, choices=CardType.choices())
