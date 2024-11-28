from common.card_type import CardType, get_main_type
from django.db import models


class Card(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, unique=True)
    main_type = models.CharField(max_length=31, null=False, choices=CardType.choices())

    @staticmethod
    def from_scryfall_card(scryfall_card):
        return Card(
            name=scryfall_card.name,
            main_type=get_main_type(scryfall_card.type_line),
        )

    class Meta:
        db_table = "card"
