from dataclasses import dataclass, field
from rootgame.shared.shared_types import ClearingInfo
from rootgame.engine.player import Character
from enum import StrEnum, auto

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
    warriors: dict[Character, int] = field(default_factory=dict)
    tokens: dict[Character, list[Token]] = field(default_factory=dict)
    suit: str = ""

    def add_token(self, character: Character, token: Token):
        self.tokens.setdefault(character, []).append(token)
    
    def add_warrior(self, character: Character, count: int = 1):
        self.warriors[character] = self.warriors.get(character, 0) + count
    
    def add_building(self, building: Building):
        self.tiles.append(building)

class Board:
    clearings: list[Clearing]

    def __init__(self):
        self.clearings = [Clearing() for _ in range(12)]
        self.clearings[0].adjacentClearings = [4, 3, 1]
        self.clearings[1].adjacentClearings = [0, 2]
        self.clearings[2].adjacentClearings = [1, 3, 7]
        self.clearings[3].adjacentClearings = [0, 5, 2]
        self.clearings[4].adjacentClearings = [0, 8, 5]
        self.clearings[5].adjacentClearings = [4, 8, 10, 6, 3]
        self.clearings[6].adjacentClearings = [5, 11, 7]
        self.clearings[7].adjacentClearings = [2, 6, 11]
        self.clearings[8].adjacentClearings = [4, 5, 9]
        self.clearings[9].adjacentClearings = [8, 10]
        self.clearings[10].adjacentClearings = [9, 5, 11]
        self.clearings[11].adjacentClearings = [6, 7, 10]
    
    def export_clearing_info(self):
        clearing_info: dict[int : ClearingInfo] = {}

        for (id, clearing) in enumerate(self.clearings):
            clearing_info[id] = ClearingInfo()
            clearing_info[id].tiles = clearing.tiles
            clearing_info[id].warriors = {key[0].upper(): value for (key, value) in clearing.warriors.items()}
            clearing_info[id].tokens = {key[0].upper(): value for (key, value) in clearing.tokens.items()}
            clearing_info[id].suit = clearing.suit

        return clearing_info
        