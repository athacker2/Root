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
    buildings: list[Building] = field(default_factory=list)
    warriors: dict[FactionName, int] = field(default_factory=dict)
    tokens: dict[FactionName, list[Token]] = field(default_factory=dict)
    suit: str = ""
    ruler: FactionName | None = None

    def add_token(self, faction: FactionName, token: Token):
        self.tokens.setdefault(faction, []).append(token)
    
    def add_warriors(self, faction: FactionName, count: int = 1):
        self.warriors[faction] = self.warriors.get(faction, 0) + count
        self.update_ruler()
    
    def get_warrior_count(self, faction: FactionName):
        return self.warriors.get(faction, 0)
    
    def remove_warriors(self, faction: FactionName, count: int = 1):
        if self.warriors.get(faction, 0) >= count:
            self.warriors[faction] = max(0, self.warriors[faction] - count)
        self.update_ruler()

    def add_building(self, building: Building):
        self.buildings.append(building)
        self.update_ruler()
    
    def is_adjacent(self, other_clearing_id: int):
        return other_clearing_id in self.adjacentClearings
    
    def update_ruler(self):
        if not self.warriors and not self.buildings:
            self.ruler = None
        else:
            # Determine the faction with the most warriors and buildings
            faction_counts: dict[FactionName, int] = {}
            for faction, count in self.warriors.items():
                faction_counts[faction] = faction_counts.get(faction, 0) + count
            for building in self.buildings:
                if building in [Building.WORKSHOP, Building.SAWMILL, Building.RECRUITER]:
                    faction_counts[FactionName.MARQUISE_DE_CAT] = faction_counts.get(FactionName.MARQUISE_DE_CAT, 0) + 1
                elif building in [Building.ROOST]:
                    faction_counts[FactionName.EYRIE_DYNASTIES] = faction_counts.get(FactionName.EYRIE_DYNASTIES, 0) + 1

            # Determine the new ruler based on the highest count
            if faction_counts:
                self.ruler = max(faction_counts, key=faction_counts.get)

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
        clearing_info: dict[int, ClearingInfo] = {}

        for (id, clearing) in enumerate(self.clearings):
            clearing_info[id] = ClearingInfo()
            clearing_info[id].tiles = clearing.buildings
            clearing_info[id].warriors = {key[0].upper(): value for (key, value) in clearing.warriors.items()}
            clearing_info[id].tokens = {key[0].upper(): value for (key, value) in clearing.tokens.items()}
            clearing_info[id].suit = clearing.suit

        return clearing_info

    def get_edges(self):
        return AUTUMN_BOARD_EDGES
        
    def move_warriors(self, faction: FactionName, numWarriors: int, startClearing: int, endClearing: int):
        self.clearings[startClearing].remove_warriors(faction, numWarriors)
        self.clearings[endClearing].add_warriors(faction, numWarriors)