from common.card_type import CardType
from django.db import models


class Card(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    main_type = models.CharField(max_length=31, null=False, choices=CardType.choices())

    class Meta:
        db_table = "card"
