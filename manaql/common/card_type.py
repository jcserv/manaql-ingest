from enum import Enum


class CardType(str, Enum):
    """
    The type of card.
    """

    Artifact = "Artifact"
    Battle = "Battle"
    Conspiracy = "Conspiracy"
    Creature = "Creature"
    Dungeon = "Dungeon"
    Enchantment = "Enchantment"
    Instant = "Instant"
    Kindred = "Kindred"
    Land = "Land"
    Phenomenon = "Phenomenon"
    Plane = "Plane"
    Planeswalker = "Planeswalker"
    Scheme = "Scheme"
    Sorcery = "Sorcery"
    Vanguard = "Vanguard"
    Unknown = "Unknown"

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]


def get_main_type(type_line: str | None) -> CardType:
    """Map Scryfall card type to our enum values."""
    if not type_line:
        return CardType.Unknown

    card_type = type_line

    # for mdfcs, set the main type to the front card
    if "//" in type_line:
        card_type = type_line.split("//")[0]

    if card_type.startswith(
        "Enchant "
    ):  # Old cards have "Enchant" instead of "Enchantment", i.e. "Enchant Creature"
        return CardType.Enchantment
    if CardType.Planeswalker.value in card_type:
        return CardType.Planeswalker
    if CardType.Battle.value in card_type:
        return CardType.Battle
    if CardType.Land.value in card_type:
        return CardType.Land
    if CardType.Creature.value in card_type:
        return CardType.Creature
    if CardType.Artifact.value in card_type:
        return CardType.Artifact
    if CardType.Enchantment.value in card_type:
        return CardType.Enchantment
    if CardType.Sorcery.value in card_type:
        return CardType.Sorcery
    if CardType.Instant.value in card_type:
        return CardType.Instant
    return CardType.Unknown
