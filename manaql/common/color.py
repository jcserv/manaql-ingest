from enum import Enum
from typing import List


class Color(str, Enum):
    """Represents a color."""

    # WUBRG
    White = "W"
    Blue = "U"
    Black = "B"
    Red = "R"
    Green = "G"

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]


def get_color(c: str) -> Color:
    """Map Scryfall color to our enum values."""
    match c:
        case "W":
            return Color.White
        case "U":
            return Color.Blue
        case "B":
            return Color.Black
        case "R":
            return Color.Red
        case "G":
            return Color.Green
        case _:
            return Color.White


def get_colors(colors: List[str]) -> List[Color]:
    """Map Scryfall colors to our enum values."""
    return [get_color(c) for c in colors]
