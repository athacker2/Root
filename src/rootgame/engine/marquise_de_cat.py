from dataclasses import dataclass, field
from rootgame.engine.faction import Faction
from rootgame.engine.board import Board, Token, Building

from rootgame.engine.types import FactionName, TurnPhase

@dataclass
class MarquiseDeCat(Faction):
    faction_name = FactionName.MARQUISE_DE_CAT

    def board_setup(self, board: Board):
        # Place keep in top left clearing (TO CHANGE W/INTERACTIVE SETUP)
        board.clearings[0].add_token(FactionName.MARQUISE_DE_CAT, Token.KEEP)

        # Place one of each building in clearings adjacent to keep
        board.clearings[4].add_building(Building.WORKSHOP)
        board.clearings[3].add_building(Building.SAWMILL)
        board.clearings[1].add_building(Building.RECRUITER)

        # Place 1 warrior in every clearing (except corner opposite to keep)
        for (id, clearing) in enumerate(board.clearings):
            if id != 11:
                clearing.add_warriors(FactionName.MARQUISE_DE_CAT, 1)

    def get_legal_actions(self, turn_phase: TurnPhase):
        # Implement logic to return legal actions for Marquise de Cat based on the turn phase
        legal_actions = ["END PHASE"]
        if turn_phase == TurnPhase.BIRDSONG:
            legal_actions.extend(["ADD WOOD TO SAWMILLS"])

        elif turn_phase == TurnPhase.DAYLIGHT:
            legal_actions.extend(["PLAY CARD #", "BATTLE X", "MOVE # # #", "RECRUIT #"])

        elif turn_phase == TurnPhase.EVENING:
            legal_actions.extend(["DRAW CARD #"])
        
        return legal_actions
    
    def add_wood_to_sawmills(self, board: Board):
        for clearing in board.clearings:
            for building in clearing.buildings:
                if building is Building.SAWMILL:
                    clearing.add_token(self.faction_name, Token.WOOD)
