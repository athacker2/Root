from dataclasses import dataclass
from typing import Protocol
from rootgame.engine.types import FactionName

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
    attacker: FactionName
    defender: FactionName
    
@dataclass
class PlayCardAction(Action):
    card_id: int

@dataclass
class RecruitAction(Action):
    clearing_id: int
    num_units: int

@dataclass
class EndPhaseAction(Action):
    pass