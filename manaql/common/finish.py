from enum import Enum
from typing import List


class Finish(str, Enum):
    """
    The available finishes of a printing, can be either nonfoil, foil, or etched.
    """

    etched = "etched"
    foil = "foil"
    nonfoil = "nonfoil"

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]


str_to_finish = {
    "nonfoil": Finish.nonfoil,
    "foil": Finish.foil,
    "etched": Finish.etched,
}


def get_finishes(finishes: List[str]) -> List[Finish]:
    """Convert Scryfall finishes to our enum values."""
    if not finishes:
        return []
    return [str_to_finish[finish.lower()] for finish in finishes]
