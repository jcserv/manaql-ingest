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
