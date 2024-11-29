from common.card_type import CardType, get_main_type
from django.test import TestCase


class TestCardType(TestCase):
    def setUp(self):
        pass

    def test_get_main_type_creature(self):
        self.assertEqual(
            get_main_type("Artifact Creature - Thopter"),
            CardType.Creature,
        )

    def test_get_main_type_planeswalker(self):
        self.assertEqual(
            get_main_type("Legendary Planeswalker - Tyvar"),
            CardType.Planeswalker,
        )

    def test_get_main_type_instant(self):
        self.assertEqual(
            get_main_type("Instant"),
            CardType.Instant,
        )

    def test_get_main_type_artifact(self):
        self.assertEqual(
            get_main_type("Artifact - Equipment"),
            CardType.Artifact,
        )

    def test_get_main_type_sorcery(self):
        self.assertEqual(
            get_main_type("Sorcery"),
            CardType.Sorcery,
        )

    def test_get_main_type_enchantment(self):
        self.assertEqual(
            get_main_type("Enchantment - Room"),
            CardType.Enchantment,
        )

    def test_get_main_type_enchantment_creature(self):
        self.assertEqual(
            get_main_type("Enchantment Creature"),
            CardType.Creature,
        )

    def test_get_main_type_enchant_creature(self):
        self.assertEqual(
            get_main_type("Enchant Creature"),
            CardType.Enchantment,
        )

    def test_get_main_type_enchant_land(self):
        self.assertEqual(
            get_main_type("Enchant Land"),
            CardType.Enchantment,
        )

    def test_get_main_type_mdfc_back_side(self):
        self.assertEqual(
            get_main_type("Sorcery // Land"),
            CardType.Sorcery,
        )
