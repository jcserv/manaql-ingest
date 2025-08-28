from common.card_type import CardType, get_main_type
from common.color import Color, get_colors
from common.format import FormatLegalities, LegalitiesField
from common.game import Game, get_games
from common.keyword import get_keywords
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Card(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, unique=True)
    main_type = models.CharField(max_length=31, null=False, choices=CardType.choices())
    type_line = models.CharField(max_length=255, null=True, blank=True)
    oracle_text = models.TextField(max_length=1024, null=True)
    keywords = ArrayField(models.CharField(max_length=127), null=True, blank=True)

    cmc = models.FloatField(null=True)
    mana_cost = models.CharField(max_length=127, null=True)
    colors = ArrayField(
        models.CharField(max_length=1, choices=Color.choices()), null=True, blank=True
    )
    color_identity = ArrayField(
        models.CharField(max_length=1, choices=Color.choices()), null=True, blank=True
    )

    power = models.CharField(max_length=15, null=True)
    toughness = models.CharField(max_length=15, null=True)

    games = ArrayField(
        models.CharField(max_length=7, choices=Game.choices()), null=True, blank=True
    )

    legalities = LegalitiesField(default=0)

    reserved = models.BooleanField(default=False)
    game_changer = models.BooleanField(default=False)

    @staticmethod
    def from_scryfall_card(scryfall_card):
        if not scryfall_card.name:
            raise ValueError("Card must have a name")

        return Card(
            name=scryfall_card.name,
            main_type=get_main_type(scryfall_card.type_line),
            type_line=scryfall_card.type_line,
            oracle_text=scryfall_card.oracle_text,
            keywords=[kw.value for kw in get_keywords(scryfall_card.keywords or [])]
            if scryfall_card.keywords
            else [],
            cmc=scryfall_card.cmc,
            mana_cost=scryfall_card.mana_cost,
            colors=[c.value for c in get_colors(scryfall_card.colors or [])]
            if scryfall_card.colors
            else [],
            color_identity=[
                c.value for c in get_colors(scryfall_card.color_identity or [])
            ]
            if scryfall_card.color_identity
            else [],
            power=scryfall_card.power,
            toughness=scryfall_card.toughness,
            games=[g.value for g in get_games(scryfall_card.games or [])]
            if scryfall_card.games
            else [],
            legalities=FormatLegalities.from_legalities(scryfall_card.legalities or {}),
            reserved=scryfall_card.reserved,
            game_changer=scryfall_card.game_changer,
        )

    class Meta:
        db_table = "card"
