from django.test import TestCase

from common.card_type import CardType
from services.card_processor import CardProcessor


class TestCardProcessor(TestCase):
    def setUp(self):
        self.processor = CardProcessor()
        self.cards_data = {
            "type_line": "Artifact Creature",
        }

    def test_map_card_type(self):
        self.assertEqual(
            self.processor.map_card_type(
                {
                    "type_line": "Artifact Creature",
                }
            ),
            CardType.Creature,
        )
