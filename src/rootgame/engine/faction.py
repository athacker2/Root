from typing import Protocol
from rootgame.engine.actions import Action
from rootgame.engine.board import Board

from rootgame.engine.player import Player
from rootgame.engine.types import FactionName, TurnPhase

class Faction(Protocol):
    faction_name: FactionName

    def board_setup(self, board: Board):
        ...
        
    def get_legal_actions(self, action: Action, current_phase: TurnPhase, player: Player, board: Board, actions_taken: list[Action]):
        ...
    
    def is_action_legal(self, action: Action, current_phase: TurnPhase, player: Player, board: Board, actions_taken: list[Action]):
        ...
    
    def apply_action(self, action: Action, board: Board, player: Player):
        ...
    
    def reset_state(self):
        ...