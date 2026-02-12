from dataclasses import dataclass
from typing import ClassVar
from rootgame.engine import actions
from rootgame.engine.faction import Faction
from rootgame.engine.player import Player
from rootgame.engine.board import Board, Token, Clearing
from rootgame.engine.building import Building, BuildingType
from rootgame.engine.actions import Action, AddWoodToSawmillsAction, EndPhaseAction, MarchAction, MarquiseRecruitAction, MarquiseBuildAction, MarquiseOverworkAction, BattleAction, DrawCardAction, DiscardCardAction, MoveAction

from rootgame.engine.types import FactionName, TurnPhase, MAX_HAND_SIZE

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

    extra_cards_to_draw: int = 0

    building_cost: ClassVar[list[int]] = [0, 1, 2, 3, 3, 4]

    sawmill_VP: ClassVar[list[int]] = [0, 1, 2, 3, 4, 5]
    workshop_VP: ClassVar[list[int]] = [0, 2, 2, 3, 4, 5]
    recruiter_VP: ClassVar[list[int]] = [0, 1, 2, 3, 3, 4]

    def board_setup(self, board: Board):
        # Place keep in top left clearing (TO CHANGE W/INTERACTIVE SETUP)
        board.clearings[0].add_token(FactionName.MARQUISE_DE_CAT, Token.KEEP)

        # Place one of each building in clearings adjacent to keep
        self.build(board, 4, BuildingType.WORKSHOP)
        self.workshops_placed += 1

        self.build(board, 3, BuildingType.SAWMILL)
        self.sawmills_placed += 1

        self.build(board, 1, BuildingType.RECRUITER)
        self.recruiters_placed += 1

        # Place 1 warrior in every clearing (except corner opposite to keep)
        for (id, clearing) in enumerate(board.clearings):
            if id != 11:
                clearing.add_warriors(FactionName.MARQUISE_DE_CAT, 1)
                self.warriors_placed += 1

    def get_legal_actions(self, turn_phase: TurnPhase, board: Board):
        # Implement logic to return legal actions for Marquise de Cat based on the turn phase
        legal_actions = ["END PHASE"]
        if turn_phase == TurnPhase.BIRDSONG:
            legal_actions.extend(["ADD WOOD"])

        elif turn_phase == TurnPhase.DAYLIGHT:
            legal_actions.extend(["BATTLE", "MARCH", "RECRUIT", "BUILD", "OVERWORK # #"])

        elif turn_phase == TurnPhase.EVENING:
            legal_actions.extend(["DRAW CARD", "DISCARD CARD"])
        
        return legal_actions
    
    def is_action_legal(self, action: Action, current_phase: TurnPhase, player: Player, board: Board, actions_taken: list[Action]):
        if(current_phase == TurnPhase.BIRDSONG):
            if(isinstance(action, AddWoodToSawmillsAction)):
                if(self.sawmills_placed == 0):
                    return False
                if sum(isinstance(a, AddWoodToSawmillsAction) for a in actions_taken) == 1:
                    return False
                return True
            
            elif(isinstance(action, EndPhaseAction)):
                if sum(isinstance(a, AddWoodToSawmillsAction) for a in actions_taken) == 0:
                    return False
                return True
            
            return False
        
        elif(current_phase == TurnPhase.DAYLIGHT):
            # Check for max of 3 actions during daylight
            if(len(actions_taken) >= 3 and not isinstance(action, EndPhaseAction)):
                return False
            
            if(isinstance(action, BattleAction)):
                return board.can_battle(action.attacker.faction.faction_name, action.defender.faction.faction_name, action.clearing_id)
            
            elif(isinstance(action, MarchAction)):
                # Validate first move
                num_warriors_one = action.move_one.num_warriors
                source_clearing_one = action.move_one.source_clearing
                destination_clearing_one = action.move_one.destination_clearing

                if(not board.can_move(self.faction_name, num_warriors_one, source_clearing_one, destination_clearing_one)):
                    return False

                # Validate second move, given first move
                num_warriors_two = action.move_two.num_warriors
                source_clearing_two = action.move_two.source_clearing
                destination_clearing_two = action.move_two.destination_clearing

                board.move_warriors(self.faction_name, num_warriors_one, source_clearing_one, destination_clearing_one) # Temporarily move warriors to validate second move
                if(not board.can_move(self.faction_name, num_warriors_two, source_clearing_two, destination_clearing_two)):
                    board.move_warriors(self.faction_name, num_warriors_one, destination_clearing_one, source_clearing_one) # Move warriors back to original clearing
                    return False
                board.move_warriors(self.faction_name, num_warriors_one, destination_clearing_one, source_clearing_one) # Move warriors back to original clearing

                return True
            
            elif(isinstance(action, MarquiseRecruitAction)):
                if(sum(isinstance(a, MarquiseRecruitAction) for a in actions_taken) == 1):
                    return False
                if(self.warriors_placed >= self.warrior_limit):
                    return False
                if(self.recruiters_placed == 0):
                    return False
                return True

            elif(isinstance(action, MarquiseBuildAction)):
                wood_needed = 0
                if(action.building_type == BuildingType.SAWMILL):
                    if(self.sawmills_placed >= self.sawmill_limit):
                        return False
                    else:
                        wood_needed = self.building_cost[self.sawmills_placed]
                elif(action.building_type == BuildingType.WORKSHOP):
                    if(self.workshops_placed >= self.workshop_limit):
                        return False
                    else:
                        wood_needed = self.building_cost[self.workshops_placed]
                elif(action.building_type == BuildingType.RECRUITER):
                    if(self.recruiters_placed >= self.recruiter_limit):
                        return False
                    else:
                        wood_needed = self.building_cost[self.recruiters_placed]
                else:
                    return False
                
                connected_clearings_with_wood = self.find_wood_in_connected_ruled_clearings(board, action.clearing_id)
                wood_available = 0
                for clearing in connected_clearings_with_wood:
                    wood_available += clearing.tokens.get(FactionName.MARQUISE_DE_CAT, []).count(Token.WOOD)
                
                if(wood_available < wood_needed):
                    return False
                return True
                
            elif(isinstance(action, MarquiseOverworkAction)):
                if(action.card_idx >= len(player.hand) or action.card_idx < 0):
                    return False
                if(board.is_valid_clearing(action.clearing_id) == False):
                    return False
                if(player.hand[action.card_idx].suit != board.clearings[action.clearing_id].suit):
                    return False
                if(len(board.get_buildings(BuildingType.SAWMILL)) == 0):
                    return False
                return True
            
            elif(isinstance(action, EndPhaseAction)):
                return True
            
            return False

        elif(current_phase == TurnPhase.EVENING):
            if(isinstance(action, DrawCardAction)):
                if sum(isinstance(a, DrawCardAction) for a in actions_taken) == 1:
                    return False
                return True
            
            elif(isinstance(action, DiscardCardAction)):
                if(len(player.hand) < MAX_HAND_SIZE):
                    return False
                if(len(player.hand) - len(action.card_ids) != MAX_HAND_SIZE):
                    return False
                if(any(card_id >= len(player.hand) or card_id < 0 for card_id in action.card_ids)):
                    return False
                return True
            
            elif(isinstance(action, EndPhaseAction)):
                if(sum(isinstance(a, DrawCardAction) for a in actions_taken) == 0):
                    return False
                if(len(player.hand) > MAX_HAND_SIZE):
                    return False
                return True
            
            return False
        
    def apply_action(self, action: Action, board: Board, player: Player):
        if isinstance(action, MoveAction):
            num_warriors = action.num_warriors
            source_clearing = action.source_clearing
            destination_clearing = action.destination_clearing
            board.move_warriors(self.faction_name, num_warriors, source_clearing, destination_clearing)
        elif isinstance(action, BattleAction):
            clearing_id = action.clearing_id
            defender = action.defender
            board.battle(self.faction_name, defender.faction.faction_name, clearing_id)
        elif isinstance(action, AddWoodToSawmillsAction):
            self.add_wood_to_sawmills(board)
        
        elif isinstance(action, MarchAction):
            self.march(board, action.move_one.num_warriors, action.move_one.source_clearing, action.move_one.destination_clearing,
                                    action.move_two.num_warriors, action.move_two.source_clearing, action.move_two.destination_clearing)
        elif(isinstance(action, MarquiseRecruitAction)):
            self.recruit(board)
            
        elif(isinstance(action, MarquiseBuildAction)):
            self.build(board, action.clearing_id, action.building_type)
        
        elif(isinstance(action, MarquiseOverworkAction)):
            self.overwork(board, action.clearing_id, player, action.card_idx)
    
    def add_wood_to_sawmills(self, board: Board):
        for clearing in board.clearings:
            for building in clearing.buildings:
                if building.type is BuildingType.SAWMILL:
                    building.used = True
                    clearing.add_token(self.faction_name, Token.WOOD)
    
    def find_wood_in_connected_ruled_clearings(self, board: Board, clearing_id: int) -> list[Clearing]:
        search_q = [board.clearings[clearing_id]]
        searched_clearings = set([clearing_id])
        clearings_with_wood = []
        while(len(search_q)):
            curr = search_q.pop()
            if(Token.WOOD in curr.tokens.get(FactionName.MARQUISE_DE_CAT, [])):
                clearings_with_wood.append(curr)
            
            # Check adj clearings that you rule
            for id in curr.adjacentClearings:
                adj_clearing = board.clearings[id]
                if(adj_clearing.ruler == FactionName.MARQUISE_DE_CAT and id not in searched_clearings):
                    search_q.append(adj_clearing)
                    searched_clearings.add(id)
        
        return clearings_with_wood 
        
    def march(self, board: Board, num_warriors_one: int, start_clearing_one: int, end_clearing_one: int,
              num_warriors_two: int, start_clearing_two: int, end_clearing_two: int):
        board.move_warriors(self.faction_name, num_warriors_one, start_clearing_one, end_clearing_one)
        board.move_warriors(self.faction_name, num_warriors_two, start_clearing_two, end_clearing_two)

    def recruit(self, board: Board):
        for clearing in board.clearings:
            for building in clearing.buildings:
                if building.type is BuildingType.RECRUITER:
                    if(self.warriors_placed < self.warrior_limit):
                        clearing.add_warriors(self.faction_name, 1)
                        self.warriors_placed += 1
    
    def build(self, board: Board, clearing_id: int, building_type: BuildingType):
        wood_needed = 0
        if(building_type is BuildingType.SAWMILL):
            wood_needed = self.building_cost[self.sawmills_placed]
        elif(building_type is BuildingType.WORKSHOP):
            wood_needed = self.building_cost[self.workshops_placed]
        elif(building_type is BuildingType.RECRUITER):
            wood_needed = self.building_cost[self.recruiters_placed]
        
        connected_clearings_with_wood = self.find_wood_in_connected_ruled_clearings(board, clearing_id)

        # Remove wood from connected clearings
        for clearing in connected_clearings_with_wood:
            while wood_needed > 0 and Token.WOOD in clearing.tokens.get(FactionName.MARQUISE_DE_CAT, []):
                clearing.tokens[FactionName.MARQUISE_DE_CAT].remove(Token.WOOD)
                wood_needed -= 1
        
        # Add building to target clearing
        board.build(clearing_id, building_type)

        if(building_type is BuildingType.SAWMILL):
            self.sawmills_placed += 1
        elif(building_type is BuildingType.WORKSHOP):
            self.workshops_placed += 1
        elif(building_type is BuildingType.RECRUITER):
            self.recruiters_placed += 1
    
    def overwork(self, board: Board, clearing_id: int, player: Player, card_idx: int):
        # Use card
        card = player.hand[card_idx]
        player.hand.pop(card_idx)  # Remove the card from player's hand

        # Add wood to sawmill at clearing
        board.clearings[clearing_id].add_token(self.faction_name, Token.WOOD)

