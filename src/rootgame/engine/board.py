from dataclasses import dataclass, field
from rootgame.engine.player import Character
from enum import Enum

class Token(Enum):
    KEEP = 1
    WOOD = 2

class Building(Enum):
    WORKSHOP = 1
    SAWMILL = 2
    RECRUITER = 3
    ROOST = 4

@dataclass
class Clearing:
    adjacentClearings: list[int] = field(default_factory=list)
    tiles: list[str] = field(default_factory=list)
    warriors: dict[Character : int] = field(default_factory=dict)
    tokens: dict[Character : list[Token]] = field(default_factory=dict)
    suit: str = ""

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
        