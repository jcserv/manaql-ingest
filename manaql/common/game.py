from enum import Enum
from typing import List


class Game(str, Enum):
    Paper = "paper"
    MTGO = "mtgo"
    Arena = "arena"

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]


def get_game(c: str) -> Game:
    match c:
        case "paper":
            return Game.Paper
        case "mtgo":
            return Game.MTGO
        case "arena":
            return Game.Arena
        case _:
            return Game.Paper


def get_games(games: List[str]) -> List[Game]:
    return [get_game(game) for game in games] if games else []
