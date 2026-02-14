from dataclasses import dataclass, field
import random
from rootgame.shared.shared_types import ClearingInfo
from rootgame.engine.types import FactionName, Suit
from rootgame.engine.building import Building, BuildingType

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
    Suit.Fox, Suit.Rabbit, Suit.Mouse,
    Suit.Rabbit, Suit.Mouse, Suit.Fox,
    Suit.Mouse, Suit.Fox, Suit.Rabbit,
    Suit.Fox, Suit.Mouse, Suit.Rabbit
]

AUTUMN_BOARD_BUILDING_LIMITS = [
    1, 2, 2,
    2, 2, 2,
    3, 2, 1,
    2, 2, 1
]

class Token(StrEnum):
    KEEP = auto()
    WOOD = auto()

@dataclass
class Clearing:
    adjacentClearings: list[int] = field(default_factory=list)
    buildings: list[Building] = field(default_factory=list)
    building_limit: int = 0
    warriors: dict[FactionName, int] = field(default_factory=dict)
    tokens: dict[FactionName, list[Token]] = field(default_factory=dict)
    suit: Suit | None = None
    ruler: FactionName | None = None

    # Clearing Methods
    def is_adjacent(self, other_clearing_id: int):
        return other_clearing_id in self.adjacentClearings
    
    # Building Methods
    def add_building(self, building: Building) -> bool:
        if(len(self.buildings) == self.building_limit):
            return False
        
        self.buildings.append(building)
        self.update_ruler()
        return True
    
    def get_buildings(self) -> list[Building]:
        return self.buildings
    
    def has_building(self, building_type: BuildingType) -> bool:
        return any(building.type == building_type for building in self.buildings)

    def can_build(self):
        return len(self.buildings) < self.building_limit
    
    def use_building(self, building_type: BuildingType) -> bool:
        if(not self.has_building(building_type=building_type)):
            return False
        
        for building in self.buildings:
            if building.type == building_type and building.used == False:
                building.used = True
                return True
        return False
        
    # Warrior Methods
    def add_warriors(self, faction: FactionName, count: int):
        self.warriors[faction] = self.warriors.get(faction, 0) + count
        self.update_ruler()
    
    def get_warrior_count(self, faction: FactionName):
        return self.warriors.get(faction, 0)

    def remove_warriors(self, faction: FactionName, count: int):
        to_remove = min(count, self.warriors.get(faction, 0))
        self.warriors[faction] = self.warriors.get(faction, 0) - to_remove
        self.update_ruler()
    
    # Token Methods
    def add_token(self, token: Token, owner: FactionName):
        self.tokens.setdefault(owner, []).append(token)
    
    # Ruler Methods
    def update_ruler(self):
        if not self.warriors and not self.buildings:
            self.ruler = None
        else:
            # Determine the faction with the most warriors and buildings
            faction_counts: dict[FactionName, int] = {}
            for faction, count in self.warriors.items():
                faction_counts[faction] = faction_counts.get(faction, 0) + count
            for building in self.buildings:
                faction_counts[building.owner] = faction_counts.get(building.owner, 0) + 1

            # Determine the new ruler based on the highest count
            if faction_counts:
                self.ruler = max(faction_counts, key=faction_counts.get)

class Board:
    clearings: list[Clearing]

    def __init__(self):
        self.clearings = [Clearing() for _ in range(len(AUTUMN_BOARD_SUITS))]

        for edge in AUTUMN_BOARD_EDGES:
            self.clearings[edge[0]].adjacentClearings.append(edge[1])
            self.clearings[edge[1]].adjacentClearings.append(edge[0])
        
        for (id, building_limit) in enumerate(AUTUMN_BOARD_BUILDING_LIMITS):
            self.clearings[id].building_limit = building_limit

        for (id, clearing) in enumerate(self.clearings):
            clearing.suit = AUTUMN_BOARD_SUITS[id]
    
    # Clearing
    def is_valid_clearing(self, clearing_id: int):
        return clearing_id >= 0 and clearing_id < len(self.clearings)
    
    def get_clearing_suit(self, clearing_id: int):
        return self.clearings[clearing_id].suit
    
    # Building Operations
    def build(self, clearing_id: int, building_type: BuildingType, owner: FactionName):
        if(self.clearings[clearing_id].can_build()):
            self.clearings[clearing_id].add_building(Building(type=building_type, owner=owner))
    
    def clearing_has_building(self, clearing_id: int, building_type: BuildingType) -> bool:
        return self.clearings[clearing_id].has_building(building_type=building_type)
    
    def mark_all_buildings_unused(self):
        for clearing in self.clearings:
            for building in clearing.buildings:
                building.used = False
    
    def get_unused_buildings_of_type(self, building_type: BuildingType):
        unused_buildings: dict[int, int] = {}
        for (id, clearing) in enumerate(self.clearings):
            for building in clearing.get_buildings():
                if(building.type == building_type):
                    unused_buildings[id] = unused_buildings.setdefault(id, 0) + 1
        return unused_buildings
    
    def use_building_at_clearing(self, clearing_id: int, building_type: BuildingType):
        if(self.clearings[clearing_id].has_building(building_type=building_type)):
            self.clearings[clearing_id].use_building(building_type)
    
    # Warrior Operations
    def move_warriors(self, faction: FactionName, numWarriors: int, startClearing: int, endClearing: int):
        self.clearings[startClearing].remove_warriors(faction, numWarriors)
        self.clearings[endClearing].add_warriors(faction, numWarriors)
    
    def can_move(self, faction: FactionName, numWarriors: int, source_clearing: int, dest_clearing: int):
        if(not self.is_valid_clearing(source_clearing) or not self.is_valid_clearing(dest_clearing)):
            print("Not a valid source clearing")
            return False
        if(numWarriors <= 0):
            print("Can't move 0 or negative warriors")
            return False
        if(not self.clearings[source_clearing].is_adjacent(dest_clearing)):
            print("Can't move between non-adj clearings")
            return False
        if(self.clearings[source_clearing].get_warrior_count(faction) < numWarriors):
            print("Insufficient warriors at clearing")
            return False
        if(not self.clearings[source_clearing].ruler == faction and not self.clearings[dest_clearing].ruler == faction):
            print("Don't rule either clearing involved in move")
            return False
        
        return True
    
    def can_battle(self, attacker: FactionName, defender: FactionName, clearing_id: int):
        if(not self.is_valid_clearing(clearing_id)):
            print("Not a valid clearing")
            return False
        if(attacker == defender):
            print("Can't battle yourself")
            return False
        
        clearing = self.clearings[clearing_id]
        if(clearing.get_warrior_count(attacker) <= 0 or clearing.get_warrior_count(defender) <= 0):
            print("Either attacker or defender has no warriors")
            return False

        return True
    
    def battle(self, attacker: FactionName, defender: FactionName, clearing_id: int):
        battle_clearing = self.clearings[clearing_id]
        rolls = [random.randint(0, 3) for _ in range(2)]

        attack_hits = min(max(rolls), battle_clearing.get_warrior_count(attacker))
        defense_hits = min(min(rolls), battle_clearing.get_warrior_count(defender))

        battle_clearing.remove_warriors(attacker, defense_hits)
        battle_clearing.remove_warriors(defender, attack_hits)
    
    # Token Operations
    def add_token(self, clearing_id: int, token: Token, owner: FactionName):
        self.clearings[clearing_id].add_token(token=token, owner=owner)
    
    # Misc Operations
    def export_clearing_info(self):
        clearing_info: dict[int, ClearingInfo] = {}

        for (id, clearing) in enumerate(self.clearings):
            clearing_info[id] = ClearingInfo()
            clearing_info[id].tiles = [building.type for building in clearing.buildings]
            clearing_info[id].warriors = {key[0].upper(): value for (key, value) in clearing.warriors.items()}
            clearing_info[id].tokens = {key[0].upper(): value for (key, value) in clearing.tokens.items()}
            clearing_info[id].suit = clearing.suit

        return clearing_info

    def get_edges(self):
        return AUTUMN_BOARD_EDGES