from common.card_type import CardType
from django.test import TestCase
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
                    "type_line": "Artifact Creature - Thopter",
                }
            ),
            CardType.Creature,
        )

        self.assertEqual(
            self.processor.map_card_type(
                {
                    "type_line": "Legendary Planeswalker - Tyvar",
                }
            ),
            CardType.Planeswalker,
        )

        self.assertEqual(
            self.processor.map_card_type(
                {
                    "type_line": "Instant",
                }
            ),
            CardType.Instant,
        )

        self.assertEqual(
            self.processor.map_card_type(
                {
                    "type_line": "Artifact - Equipment",
                }
            ),
            CardType.Artifact,
        )

        self.assertEqual(
            self.processor.map_card_type(
                {
                    "type_line": "Sorcery",
                }
            ),
            CardType.Sorcery,
        )

        self.assertEqual(
            self.processor.map_card_type(
                {
                    "type_line": "Enchantment - Room",
                }
            ),
            CardType.Enchantment,
        )

        # TODO: Fix this?
        # self.assertEqual(
        #     self.processor.map_card_type(
        #         {
        #             "type_line": "Enchant Creature",
        #         }
        #     ),
        #     CardType.Enchantment,
        # )

        # self.assertEqual(
        #     self.processor.map_card_type(
        #         {
        #             "type_line": "Enchant Land",
        #         }
        #     ),
        #     CardType.Enchantment,
        # )

        # self.assertEqual(
        #     self.processor.map_card_type(
        #         {
        #             "type_line": "Sorcery // Land",
        #         }
        #     ),
        #     CardType.Sorcery,
        # )
