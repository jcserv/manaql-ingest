from enum import Enum


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
