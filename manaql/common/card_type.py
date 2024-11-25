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


def get_main_type(type_line: str) -> CardType:
    """Map Scryfall card type to our enum values."""
    if not type_line:
        return CardType.Unknown
    if type_line.startswith(
        "Enchant "
    ):  # Old cards have "Enchant" instead of "Enchantment", i.e. "Enchant Creature"
        return CardType.Enchantment
    if CardType.Planeswalker.value in type_line:
        return CardType.Planeswalker
    if CardType.Battle.value in type_line:
        return CardType.Battle
    if CardType.Land.value in type_line:
        return CardType.Land
    if CardType.Creature.value in type_line:
        return CardType.Creature
    if CardType.Artifact.value in type_line:
        return CardType.Artifact
    if CardType.Enchantment.value in type_line:
        return CardType.Enchantment
    if CardType.Sorcery.value in type_line:
        return CardType.Sorcery
    if CardType.Instant.value in type_line:
        return CardType.Instant
    return CardType.Unknown
