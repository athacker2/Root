from dataclasses import dataclass, field
from rootgame.engine.faction import Faction
from rootgame.engine.board import Board
from rootgame.engine.building import BuildingType

from rootgame.engine.types import FactionName, TurnPhase

@dataclass
class EyrieDynasties(Faction):
    faction_name = FactionName.EYRIE_DYNASTIES

    def board_setup(self, board: Board):
        # Place roost in bottom right
        board.build(11, BuildingType.ROOST)

        # Place 6 warriors in starting clearing
        board.clearings[11].add_warriors(FactionName.EYRIE_DYNASTIES, 6)
    
    def get_legal_actions(self, turn_phase: TurnPhase):
         # Implement logic to return legal actions for Eyrie Dynasties based on the turn phase
        legal_actions = ["END PHASE"]
        if turn_phase == TurnPhase.BIRDSONG:
            legal_actions.extend([])

        elif turn_phase == TurnPhase.DAYLIGHT:
            legal_actions.extend(["PLAY CARD #", "BATTLE X", "MOVE # # #", "RECRUIT #"])

        elif turn_phase == TurnPhase.EVENING:
            legal_actions.extend(["DRAW CARD #"])
        
        return legal_actions