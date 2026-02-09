from enum import StrEnum, auto
from typing import Protocol
from rootgame.engine.board import Board

from rootgame.engine.types import FactionName, TurnPhase

class Faction(Protocol):
    faction_name: FactionName

    def board_setup(self, board: Board):
        ...
        
    def get_legal_actions(self, turn_phase: TurnPhase):
        ...