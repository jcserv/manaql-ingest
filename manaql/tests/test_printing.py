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

    def test_printing_get_image_uris_normal(self):
        normal_card = ScryfallCard(
            image_uris={
                "normal": "https://cards.scryfall.io/normal/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
                "large": "https://cards.scryfall.io/large/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
            }
        )
        image_uri, back_image_uri = Printing.get_image_uris(normal_card)
        self.assertEqual(
            image_uri,
            "https://cards.scryfall.io/normal/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
        )
        self.assertEqual(back_image_uri, None)

    def test_printing_get_image_uris_mdfc(self):
        mdfc_card = ScryfallCard(
            card_faces=[
                {
                    "image_uris": {
                        "normal": "https://cards.scryfall.io/normal/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
                        "large": "https://cards.scryfall.io/large/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
                    }
                },
                {
                    "image_uris": {
                        "normal": "https://cards.scryfall.io/normal/back/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
                        "large": "https://cards.scryfall.io/large/back/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
                    }
                },
            ]
        )
        image_uri, back_image_uri = Printing.get_image_uris(mdfc_card)
        self.assertEqual(
            image_uri,
            "https://cards.scryfall.io/normal/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
        )
        self.assertEqual(
            back_image_uri,
            "https://cards.scryfall.io/normal/back/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
        )
