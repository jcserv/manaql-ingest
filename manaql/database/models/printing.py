from common.finish import Finish
from django.contrib.postgres.fields import ArrayField
from django.db import models

from database.models.card import Card


class Printing(models.Model):
    id = models.AutoField(primary_key=True)
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE)
    set_code = models.CharField(max_length=7, null=False, db_column="set")
    set_name = models.CharField(max_length=255, null=False)
    collector_number = models.CharField(max_length=7, null=False)

    image_uri = models.CharField(max_length=255, null=False)
    back_image_uri = models.CharField(max_length=255, null=True)
    finishes = ArrayField(models.CharField(max_length=7, choices=Finish.choices()))

    price_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_usd_foil = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_usd_etched = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_eur = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_eur_foil = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_eur_etched = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        db_table = "printing"
