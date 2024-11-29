from database.models.printing import Printing
from database.models.scryfall_card import ScryfallCard
from django.test import TestCase


class TestPrinting(TestCase):
    def test_printing_is_card_serialized(self):
        serialized_card = ScryfallCard(
            promo_types=["serialized"],
        )
        self.assertTrue(Printing.is_card_serialized(serialized_card))
        not_serialized_card = ScryfallCard(
            promo_types=[],
        )
        self.assertFalse(Printing.is_card_serialized(not_serialized_card))
