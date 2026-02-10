from dataclasses import dataclass
from typing import ClassVar
from rootgame.engine.faction import Faction
from rootgame.engine.board import Board, Token, Building

from rootgame.engine.types import FactionName, TurnPhase

@dataclass
class MarquiseDeCat(Faction):
    faction_name: ClassVar[FactionName] = FactionName.MARQUISE_DE_CAT

    warrior_limit: ClassVar[int] = 25 # Starting number of warriors for Marquise de Cat
    warriors_placed: int = 0

    sawmill_limit: ClassVar[int] = 6
    sawmills_placed: int = 0

    workshop_limit: ClassVar[int] = 6
    workshops_placed: int = 0

    recruiter_limit: ClassVar[int] = 6
    recruiters_placed: int = 0

    building_cost: ClassVar[list[int]] = [0, 1, 2, 3, 3, 4]

    sawmill_VP: ClassVar[list[int]] = [0, 1, 2, 3, 4, 5]
    workshop_VP: ClassVar[list[int]] = [0, 2, 2, 3, 4, 5]
    recruiter_VP: ClassVar[list[int]] = [0, 1, 2, 3, 3, 4]

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
    
    def march(self, board: Board, num_warriors_one: int, start_clearing_one: int, end_clearing_one: int,
              num_warriors_two: int, start_clearing_two: int, end_clearing_two: int):
        board.move_warriors(self.faction_name, num_warriors_one, start_clearing_one, end_clearing_one)
        board.move_warriors(self.faction_name, num_warriors_two, start_clearing_two, end_clearing_two)

    def recruit(self, board: Board):
        for clearing in board.clearings:
            for building in clearing.buildings:
                if building is Building.RECRUITER:
                    if(self.warrior_supply):
                        clearing.add_warriors(self.faction_name, 1)
                        self.warrior_supply -= 1
    
    def build(self, board: Board, clearing_id: int, building: Building):
        if(building is Building.SAWMILL):
            pass
        elif(building is Building.WORKSHOP):
            pass
        elif(building is Building.RECRUITER):
            pass
