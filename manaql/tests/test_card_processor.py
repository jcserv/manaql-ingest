from common.scryfall import ImageURIs, Prices, SFCard
from database.models.card import Card
from database.models.printing import Printing
from django.test import TestCase
from services.card_processor import CardProcessor


class TestCardProcessor(TestCase):
    def setUp(self):
        self.processor = CardProcessor()

    def test_process_cards_should_handle_multiple_printings(self):
        cards_data = [
            SFCard(
                name="Forest",
                type_line="Basic Land \u2014 Forest",
                set="blb",
                set_name="Bloomburrow",
                collector_number="280",
                image_uris=ImageURIs(
                    small="https://cards.scryfall.io/small/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
                    normal="https://cards.scryfall.io/normal/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
                    large="https://cards.scryfall.io/large/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
                    png="https://cards.scryfall.io/png/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.png?1721427487",
                    art_crop="https://cards.scryfall.io/art_crop/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
                    border_crop="https://cards.scryfall.io/border_crop/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
                ),
                finishes=["nonfoil", "foil"],
                prices=Prices(
                    usd="0.21",
                    usd_foil="0.47",
                    usd_etched=None,
                    eur=None,
                    eur_foil=None,
                    tix="0.02",
                ),
            ),
            SFCard(
                name="Forest",
                type_line="Basic Land \u2014 Forest",
                set="ddr",
                set_name="Duel Decks: Nissa vs. Ob Nixilis",
                collector_number="35",
                image_uris=ImageURIs(
                    small="https://cards.scryfall.io/small/front/0/0/006e0990-0596-4537-aced-51ac499938af.jpg?1562229259",
                    normal="https://cards.scryfall.io/normal/front/0/0/006e0990-0596-4537-aced-51ac499938af.jpg?1562229259",
                    large="https://cards.scryfall.io/large/front/0/0/006e0990-0596-4537-aced-51ac499938af.jpg?1562229259",
                    png="https://cards.scryfall.io/png/front/0/0/006e0990-0596-4537-aced-51ac499938af.png?1562229259",
                    art_crop="https://cards.scryfall.io/art_crop/front/0/0/006e0990-0596-4537-aced-51ac499938af.jpg?1562229259",
                    border_crop="https://cards.scryfall.io/border_crop/front/0/0/006e0990-0596-4537-aced-51ac499938af.jpg?1562229259",
                ),
                finishes=["nonfoil"],
                prices=Prices(
                    usd="0.12",
                    usd_foil=None,
                    usd_etched=None,
                    eur="0.05",
                    eur_foil=None,
                    tix=None,
                ),
            ),
        ]
        self.processor.process_cards(cards_data)
        self.assertEqual(Card.objects.count(), 1)
        self.assertEqual(Printing.objects.count(), 2)
