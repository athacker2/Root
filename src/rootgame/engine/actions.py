from dataclasses import dataclass
from typing import Protocol
from rootgame.engine.types import DecreeOption
from rootgame.engine.player import Player
from rootgame.engine.building import BuildingType

class Action(Protocol):
    pass

@dataclass
class MoveAction(Action):
    num_warriors: int
    source_clearing: int
    destination_clearing: int

@dataclass
class BattleAction(Action):
    clearing_id: int
    attacker: Player
    defender: Player
    
@dataclass
class PlayCardAction(Action):
    card_id: int

@dataclass
class DrawCardAction(Action):
    pass

@dataclass 
class DiscardCardAction(Action):
    card_ids: list[int]

@dataclass
class RecruitAction(Action):
    clearing_id: int
    num_units: int

@dataclass
class EndPhaseAction(Action):
    pass

# Marquise De Cat Actions
@dataclass
class AddWoodToSawmillsAction(Action):
    pass

@dataclass
class MarchAction(Action):
    move_one: MoveAction
    move_two: MoveAction

@dataclass
class MarquiseRecruitAction(Action):
    pass

@dataclass
class MarquiseBuildAction(Action):
    clearing_id : int
    building_type: BuildingType

@dataclass 
class MarquiseOverworkAction(Action):
    clearing_id: int
    card_idx: int

# Eyrie Dynasties Actions
@dataclass
class EyrieAddToDecreeAction(Action):
    card_id: int
    decree_option: DecreeOption

@dataclass
class EyrieRecruitAction(Action):
    clearing_id: int

@dataclass
class EyrieMoveAction(Action):
    num_warriors: int
    source_clearing: int
    destination_clearing: int
    
@dataclass 
class EyrieBattleAction(Action):
    clearing_id: int
    attacker: Player
    defender: Player

@dataclass 
class EyrieBuildAction(Action):
    clearing_id : int