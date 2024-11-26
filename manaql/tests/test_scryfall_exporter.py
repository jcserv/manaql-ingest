from database.models.scryfall_card import ScryfallCard
from django.test import TestCase
from services.scryfall_exporter import ScryfallExporter, SequentialStrategy, filterCard


class TestCardProcessor(TestCase):
    def setUp(self):
        self.exporter = ScryfallExporter()
        self.strategy = SequentialStrategy()
        self.default_valid_card = {
            "lang": "en",
            "layout": "normal",
            "games": ["paper"],
        }

    def test_filter_should_filter_out_art_series(self):
        self.assertFalse(
            filterCard(
                {
                    **self.default_valid_card,
                    "layout": "normal",
                }
            )
        )
        self.assertTrue(
            filterCard(
                {
                    **self.default_valid_card,
                    "layout": "token",
                }
            )
        )
        self.assertTrue(
            filterCard(
                {
                    **self.default_valid_card,
                    "layout": "art_series",
                }
            )
        )

    def test_filter_should_filter_out_non_english(self):
        self.assertFalse(filterCard({**self.default_valid_card, "lang": "en"}))
        self.assertTrue(filterCard({**self.default_valid_card, "lang": None}))
        all_non_eng_langs = [
            "ar",
            "de",
            "es",
            "fr",
            "grc",
            "he",
            "it",
            "ja",
            "ko",
            "la",
            "ph",
            "pt",
            "ru",
            "sa",
            "zhs",
            "zht",
        ]

        for lang in all_non_eng_langs:
            self.assertTrue(filterCard({**self.default_valid_card, "lang": lang}))

    def test_filter_should_filter_out_non_paper_cards(self):
        self.assertTrue(
            filterCard(
                {
                    **self.default_valid_card,
                    "games": ["mtgo"],
                }
            )
        )
        self.assertFalse(
            filterCard(
                {
                    **self.default_valid_card,
                    "games": ["paper"],
                }
            )
        )
        self.assertFalse(
            filterCard(
                {
                    **self.default_valid_card,
                    "games": ["paper", "mtgo"],
                }
            )
        )

    def test_process_cards_should_handle_empty_list(self):
        self.exporter.process_cards([], self.strategy)
        self.assertEqual(ScryfallCard.objects.count(), 0)

    def test_process_cards_should_handle_scryfall_card_object(self):
        cards_data = [
            {
                "object": "card",
                "id": "0000419b-0bba-4488-8f7a-6194544ce91e",
                "oracle_id": "b34bb2dc-c1af-4d77-b0b3-a0fb342a5fc6",
                "multiverse_ids": [668564],
                "mtgo_id": 129825,
                "arena_id": 91829,
                "tcgplayer_id": 558404,
                "name": "Forest",
                "lang": "en",
                "released_at": "2024-08-02",
                "uri": "https://api.scryfall.com/cards/0000419b-0bba-4488-8f7a-6194544ce91e",
                "scryfall_uri": "https://scryfall.com/card/blb/280/forest?utm_source=api",
                "layout": "normal",
                "highres_image": True,
                "image_status": "highres_scan",
                "image_uris": {
                    "small": "https://cards.scryfall.io/small/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
                    "normal": "https://cards.scryfall.io/normal/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
                    "large": "https://cards.scryfall.io/large/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
                    "png": "https://cards.scryfall.io/png/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.png?1721427487",
                    "art_crop": "https://cards.scryfall.io/art_crop/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
                    "border_crop": "https://cards.scryfall.io/border_crop/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
                },
                "mana_cost": "",
                "cmc": 0.0,
                "type_line": "Basic Land \u2014 Forest",
                "oracle_text": "({T}: Add {G}.)",
                "colors": [],
                "color_identity": ["G"],
                "keywords": [],
                "produced_mana": ["G"],
                "legalities": {
                    "standard": "legal",
                    "future": "legal",
                    "historic": "legal",
                    "timeless": "legal",
                    "gladiator": "legal",
                    "pioneer": "legal",
                    "explorer": "legal",
                    "modern": "legal",
                    "legacy": "legal",
                    "pauper": "legal",
                    "vintage": "legal",
                    "penny": "legal",
                    "commander": "legal",
                    "oathbreaker": "legal",
                    "standardbrawl": "legal",
                    "brawl": "legal",
                    "alchemy": "legal",
                    "paupercommander": "legal",
                    "duel": "legal",
                    "oldschool": "not_legal",
                    "premodern": "legal",
                    "predh": "legal",
                },
                "games": ["paper", "mtgo", "arena"],
                "reserved": False,
                "foil": True,
                "nonfoil": True,
                "finishes": ["nonfoil", "foil"],
                "oversized": False,
                "promo": False,
                "reprint": True,
                "variation": False,
                "set_id": "a2f58272-bba6-439d-871e-7a46686ac018",
                "set": "blb",
                "set_name": "Bloomburrow",
                "set_type": "expansion",
                "set_uri": "https://api.scryfall.com/sets/a2f58272-bba6-439d-871e-7a46686ac018",
                "set_search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Ablb&unique=prints",
                "scryfall_set_uri": "https://scryfall.com/sets/blb?utm_source=api",
                "rulings_uri": "https://api.scryfall.com/cards/0000419b-0bba-4488-8f7a-6194544ce91e/rulings",
                "prints_search_uri": "https://api.scryfall.com/cards/search?order=released&q=oracleid%3Ab34bb2dc-c1af-4d77-b0b3-a0fb342a5fc6&unique=prints",
                "collector_number": "280",
                "digital": False,
                "rarity": "common",
                "card_back_id": "0aeebaf5-8c7d-4636-9e82-8c27447861f7",
                "artist": "David Robert Hovey",
                "artist_ids": ["22ab27e3-6476-48f1-a9f7-9a9e86339030"],
                "illustration_id": "fb2b1ca2-7440-48c2-81c8-84da0a45a626",
                "border_color": "black",
                "frame": "2015",
                "full_art": True,
                "textless": False,
                "booster": True,
                "story_spotlight": False,
                "prices": {
                    "usd": "0.21",
                    "usd_foil": "0.47",
                    "usd_etched": None,
                    "eur": None,
                    "eur_foil": None,
                    "tix": "0.02",
                },
                "related_uris": {
                    "gatherer": "https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=668564&printed=False",
                    "tcgplayer_infinite_articles": "https://tcgplayer.pxf.io/c/4931599/1830156/21018?subId1=api&trafcat=infinite&u=https%3A%2F%2Finfinite.tcgplayer.com%2Fsearch%3FcontentMode%3Darticle%26game%3Dmagic%26partner%3Dscryfall%26q%3DForest",
                    "tcgplayer_infinite_decks": "https://tcgplayer.pxf.io/c/4931599/1830156/21018?subId1=api&trafcat=infinite&u=https%3A%2F%2Finfinite.tcgplayer.com%2Fsearch%3FcontentMode%3Ddeck%26game%3Dmagic%26partner%3Dscryfall%26q%3DForest",
                    "edhrec": "https://edhrec.com/route/?cc=Forest",
                },
                "purchase_uris": {
                    "tcgplayer": "https://tcgplayer.pxf.io/c/4931599/1830156/21018?subId1=api&u=https%3A%2F%2Fwww.tcgplayer.com%2Fproduct%2F558404%3Fpage%3D1",
                    "cardmarket": "https://www.cardmarket.com/en/Magic/Products/Search?referrer=scryfall&searchString=Forest&utm_campaign=card_prices&utm_medium=text&utm_source=scryfall",
                    "cardhoarder": "https://www.cardhoarder.com/cards/129825?affiliate_id=scryfall&ref=card-profile&utm_campaign=affiliate&utm_medium=card&utm_source=scryfall",
                },
            },
        ]
        self.exporter.process_cards(cards_data, self.strategy)
        self.assertEqual(ScryfallCard.objects.count(), 1)
