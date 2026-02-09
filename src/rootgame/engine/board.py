from dataclasses import dataclass, field
from rootgame.shared.shared_types import ClearingInfo
from rootgame.engine.types import FactionName

from enum import StrEnum, auto

AUTUMN_BOARD_EDGES = [
    (0, 1), (0, 3), (0, 4),
    (1, 2),
    (2, 3), (2, 7),
    (3, 5),
    (4, 5), (4, 8),
    (5, 6), (5, 8), (5, 10),
    (6, 7), (6, 11),
    (7, 11),
    (8, 9),
    (9, 10),
    (10, 11),
]

AUTUMN_BOARD_SUITS = [
    "fox", "rabbit", "mouse",
    "rabbit", "mouse", "fox",
    "mouse", "fox", "rabbit",
    "fox", "mouse", "rabbit"
]

class Token(StrEnum):
    KEEP = auto()
    WOOD = auto()

class Building(StrEnum):
    WORKSHOP = auto()
    SAWMILL = auto()
    RECRUITER = auto()
    ROOST = auto()

@dataclass
class Clearing:
    adjacentClearings: list[int] = field(default_factory=list)
    tiles: list[Building] = field(default_factory=list)
    warriors: dict[FactionName, int] = field(default_factory=dict)
    tokens: dict[FactionName, list[Token]] = field(default_factory=dict)
    suit: str = ""

    def add_token(self, faction: FactionName, token: Token):
        self.tokens.setdefault(faction, []).append(token)
    
    def add_warriors(self, faction: FactionName, count: int = 1):
        self.warriors[faction] = self.warriors.get(faction, 0) + count
    
    def get_warrior_count(self, faction: FactionName):
        return self.warriors.get(faction, 0)
    
    def remove_warriors(self, faction: FactionName, count: int = 1):
        if self.warriors.get(faction, 0) >= count:
            self.warriors[faction] = max(0, self.warriors[faction] - count)

    
    def add_building(self, building: Building):
        self.tiles.append(building)
    
    def isAdjacent(self, other_clearing_id: int):
        return other_clearing_id in self.adjacentClearings

class Board:
    clearings: list[Clearing]

    def __init__(self):
        self.clearings = [Clearing() for _ in range(12)]

        for edge in AUTUMN_BOARD_EDGES:
            self.clearings[edge[0]].adjacentClearings.append(edge[1])
            self.clearings[edge[1]].adjacentClearings.append(edge[0])

        for (id, clearing) in enumerate(self.clearings):
            clearing.suit = AUTUMN_BOARD_SUITS[id]
    
    def export_clearing_info(self):
        clearing_info: dict[int : ClearingInfo] = {}

        for (id, clearing) in enumerate(self.clearings):
            clearing_info[id] = ClearingInfo()
            clearing_info[id].tiles = clearing.tiles
            clearing_info[id].warriors = {key[0].upper(): value for (key, value) in clearing.warriors.items()}
            clearing_info[id].tokens = {key[0].upper(): value for (key, value) in clearing.tokens.items()}
            clearing_info[id].suit = clearing.suit

        return clearing_info

    def get_edges(self):
        return AUTUMN_BOARD_EDGES
        