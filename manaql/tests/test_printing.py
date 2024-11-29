from database.models.printing import Printing
from database.models.scryfall_card import ScryfallCard
from django.test import TestCase


class TestPrinting(TestCase):
    def test_printing_is_card_serialized(self):
        serialized_card = ScryfallCard(
            collector_number="99z",
        )
        self.assertTrue(Printing.is_card_serialized(serialized_card))

    # def test_printing_is_serialized_works_with_exceptions(self):
    #     exceptions = [
    #         ScryfallCard(
    #             set="inr",
    #             collector_number="491",
    #         ),
    #     ]
