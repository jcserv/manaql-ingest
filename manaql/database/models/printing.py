import re

from common.finish import Finish, get_finishes
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Printing(models.Model):
    id = models.AutoField(primary_key=True)
    card = models.ForeignKey("Card", on_delete=models.CASCADE)
    set_code = models.CharField(max_length=7, null=False, db_column="set")
    set_name = models.CharField(max_length=255, null=False)
    collector_number = models.CharField(max_length=31, null=False)
    is_serialized = models.BooleanField(default=False)

    image_uri = models.CharField(max_length=255, null=False)
    back_image_uri = models.CharField(max_length=255, null=True)
    finishes = ArrayField(models.CharField(max_length=7, choices=Finish.choices()))

    price_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_usd_foil = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_usd_etched = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_eur = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_eur_foil = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_eur_etched = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    @staticmethod
    def is_card_serialized(scryfall_card) -> bool:
        if not scryfall_card.collector_number:
            return False
        return bool(re.match(r"^\d+z$", scryfall_card.collector_number))

    @staticmethod
    def get_image_uris(scryfall_card) -> tuple[str | None, str | None]:
        """Extract normal and back image URIs from card data."""
        image_uri = None
        back_image_uri = None

        if scryfall_card.image_uris:
            image_uri = scryfall_card.image_uris.get("normal", "")
        elif scryfall_card.card_faces and len(scryfall_card.card_faces) > 0:
            if scryfall_card.card_faces[0].image_uris:
                image_uri = scryfall_card.card_faces[0].image_uris.get("normal", "")
            if (
                len(scryfall_card.card_faces) > 1
                and scryfall_card.card_faces[1].image_uris
            ):
                back_image_uri = scryfall_card.card_faces[1].image_uris.get(
                    "normal", ""
                )
        return image_uri, back_image_uri

    @staticmethod
    def from_scryfall_card(card_id: int, scryfall_card):
        image_uri, back_image_uri = Printing.get_image_uris(scryfall_card)

        return Printing(
            card_id=card_id,
            set_code=scryfall_card.set_code,
            set_name=scryfall_card.set_name,
            collector_number=scryfall_card.collector_number,
            is_serialized=Printing.is_card_serialized(scryfall_card),
            image_uri=image_uri,
            back_image_uri=back_image_uri,
            finishes=get_finishes(scryfall_card.finishes),
            price_usd=scryfall_card.prices.get("usd", ""),
            price_usd_foil=scryfall_card.prices.get("usd_foil", ""),
            price_usd_etched=scryfall_card.prices.get("usd_etched", ""),
            price_eur=scryfall_card.prices.get("eur", ""),
            price_eur_foil=scryfall_card.prices.get("eur_foil", ""),
            price_eur_etched=None,  # This will be computed in the API
        )

    class Meta:
        db_table = "printing"
