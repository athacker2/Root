from dataclasses import dataclass, field
from enum import StrEnum, auto
from typing import ClassVar
import random

from rootgame.engine.actions import Action, DiscardCardAction, DrawCardAction, EndPhaseAction, EyrieAddToDecreeAction, EyrieBattleAction, EyrieMoveAction, EyrieRecruitAction, EyrieBuildAction, EyrieTurmoilAction, EyrieCraftAction
from rootgame.engine.card import Card, VizierCard, ItemCard
from rootgame.engine.faction import Faction
from rootgame.engine.board import Board
from rootgame.engine.building import BuildingType
from rootgame.engine.player import Player

from rootgame.engine.types import MAX_HAND_SIZE, FactionName, Suit, TurnPhase, DecreeOption, EyrieLeader

LEADER_VIZIERS = {
    EyrieLeader.DESPOT: [DecreeOption.Move, DecreeOption.Build],
    EyrieLeader.COMMANDER: [DecreeOption.Move, DecreeOption.Battle],
    EyrieLeader.CHARISMATIC: [DecreeOption.Recruit, DecreeOption.Battle],
    EyrieLeader.BUILDER: [DecreeOption.Recruit, DecreeOption.Move]
}

@dataclass
class EyrieDynasties(Faction):
    faction_name = FactionName.EYRIE_DYNASTIES

    leader: EyrieLeader | None = None
    used_leaders: list[EyrieLeader] = field(default_factory=list)

    decree: dict[DecreeOption, list[Card]] = field(default_factory=dict)
    decree_actions_taken: dict[DecreeOption, list[Card]] = field(default_factory=dict)

    warrior_limit: ClassVar[int] = 20
    warriors_placed: int = 0

    roost_limit: ClassVar[int] = 7
    roosts_placed: int = 0


    def board_setup(self, board: Board):
        # Place roost in bottom right
        board.build(11, BuildingType.ROOST)
        self.roosts_placed += 1

        # Place 6 warriors in starting clearing
        board.clearings[11].add_warriors(FactionName.EYRIE_DYNASTIES, 6)
        self.warriors_placed += 6

        # Set decree based on leader
        self.set_leader_viziers()
    
    def get_legal_actions(self, turn_phase: TurnPhase, board: Board):
         # Implement logic to return legal actions for Eyrie Dynasties based on the turn phase
        legal_actions = ["END PHASE"]
        if turn_phase == TurnPhase.BIRDSONG:
            legal_actions.extend(["ADD TO DECREE"])

        elif turn_phase == TurnPhase.DAYLIGHT:
            legal_actions.extend(["RECRUIT", "MOVE", "BATTLE", "BUILD"])

        elif turn_phase == TurnPhase.EVENING:
            legal_actions.extend(["DRAW CARD", "DISCARD CARD"])
        
        return legal_actions
    
    def is_action_legal(self, action: Action, current_phase: TurnPhase, player: Player, board: Board, actions_taken: list[Action]):
        if(current_phase == TurnPhase.BIRDSONG):
            if(isinstance(action, EyrieAddToDecreeAction)):
                if(sum(isinstance(a, EyrieAddToDecreeAction) for a in actions_taken) == 2):
                    return False
                if(action.card_id >= len(player.hand) or action.card_id < 0):
                    return False
                if(action.decree_option not in DecreeOption):
                    return False
                return True
            
            elif(isinstance(action, EndPhaseAction)):
                if(sum(isinstance(a, EyrieAddToDecreeAction) for a in actions_taken) == 0):
                    return False
                return True
            
            return False
        
        elif(current_phase == TurnPhase.DAYLIGHT):
            # If turmoiled, can only end phase
            if(len(actions_taken) and isinstance(actions_taken[-1], EyrieTurmoilAction)):
                if(isinstance(action, EndPhaseAction)):
                    return True
                return False
            
            # Can always turmoil during daylight (for now)
            if(isinstance(action, EyrieTurmoilAction)):
                return True
        
            # Must do all crafting at start (first action, or following another craft actions)
            if(isinstance(action, EyrieCraftAction)):
                print("Validating craft")
                if(action.card_idx >= len(player.hand) or action.card_idx < 0):
                    print("Invalid card index")
                    return False
                if(not len(actions_taken) == 0):
                    print(actions_taken)
                    if(not isinstance(actions_taken[-1], EyrieCraftAction)):
                        print("Not start of turn")
                        return False
                if(not isinstance(player.hand[action.card_idx], ItemCard)):
                    print("Not item card")
                    return False
                
                # Check if have enough unused workshops
                card_to_craft: ItemCard = player.hand[action.card_idx]
                if(not board.verify_crafting_requirements(building_type=BuildingType.ROOST, crafting_requirements=card_to_craft.crafting_requirements)):
                    print("Not enough roosts")
                    return False
                
                return True
            
            # If recruit actions left, must finish them
            if(not self.resolved_decree_option(DecreeOption.Recruit)):
                if(isinstance(action, EyrieRecruitAction)):
                    if(not board.is_valid_clearing(action.clearing_id)):
                        return False
                    if(DecreeOption.Recruit not in self.decree or len(self.decree.get(DecreeOption.Recruit, [])) == 0):
                        return False
                    if(not self.suit_exists_in_decree_option(DecreeOption.Recruit, board.clearings[action.clearing_id].suit)):
                        return False
                    if(not board.clearings[action.clearing_id].has_building(BuildingType.ROOST)):
                        return False
                    if(self.warriors_placed == self.warrior_limit):
                        return False
                    return True
                return False
            
            elif(not self.resolved_decree_option(DecreeOption.Move)):
                if(isinstance(action, EyrieMoveAction)):
                    if(not board.can_move(self.faction_name, action.num_warriors, action.source_clearing, action.destination_clearing)):
                        return False
                    if(not self.suit_exists_in_decree_option(DecreeOption.Move, board.clearings[action.source_clearing].suit)):
                        return False
                    return True
                return False
            
            elif(not self.resolved_decree_option(DecreeOption.Battle)):
                if(isinstance(action, EyrieBattleAction)):
                    if(not board.can_battle(self.faction_name, action.defender.faction.faction_name, action.clearing_id)):
                        return False
                    if(not self.suit_exists_in_decree_option(DecreeOption.Battle, board.clearings[action.clearing_id].suit)):
                        return False
                    return True
                return False
            
            elif(not self.resolved_decree_option(DecreeOption.Build)):
                if(isinstance(action, EyrieBuildAction)):
                    if(not self.suit_exists_in_decree_option(DecreeOption.Build, board.clearings[action.clearing_id].suit)):
                        return False
                    if(not board.clearings[action.clearing_id].ruler == self.faction_name):
                        return False
                    if(board.clearings[action.clearing_id].has_building(BuildingType.ROOST)):
                        return False
                    if(self.roosts_placed == self.roost_limit):
                        return False
                    return True
                return False
            
            elif(isinstance(action, EndPhaseAction)):
                return True
                
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
        
        return False
    
    def apply_action(self, action: Action, board: Board, player: Player):
            if(isinstance(action, EyrieAddToDecreeAction)):
                card = player.hand[action.card_id]
                self.add_to_decree(card, action.decree_option)
                player.hand.pop(action.card_id)

            elif(isinstance(action, EyrieRecruitAction)):
                board.clearings[action.clearing_id].add_warriors(FactionName.EYRIE_DYNASTIES, 1)
                self.take_decree_action(board.clearings[action.clearing_id].suit, DecreeOption.Recruit)

            elif(isinstance(action, EyrieMoveAction)):
                board.move_warriors(self.faction_name, action.num_warriors, action.source_clearing, action.destination_clearing)
                self.take_decree_action(board.clearings[action.source_clearing].suit, DecreeOption.Move)

            elif(isinstance(action, EyrieBattleAction)):
                board.battle(self.faction_name, action.defender.faction.faction_name, action.clearing_id)
                self.take_decree_action(board.clearings[action.clearing_id].suit, DecreeOption.Battle)
                
            elif(isinstance(action, EyrieBuildAction)):
                board.build(action.clearing_id, BuildingType.ROOST)
                self.take_decree_action(board.clearings[action.clearing_id].suit, DecreeOption.Build)
            
            elif(isinstance(action, EyrieTurmoilAction)):
                self.turmoil()
            
            elif(isinstance(action, EyrieCraftAction)):
                used_card: ItemCard = player.hand.pop(action.card_idx)
                board.use_crafting_requirements(building_type=BuildingType.ROOST, crafting_requirements=used_card.crafting_requirements)

    def add_to_decree(self, card: Card, decree_option: DecreeOption):
        if decree_option not in self.decree:
            self.decree[decree_option] = []
        self.decree[decree_option].append(card)
    
    def get_remaining_decree(self, decree_option: DecreeOption):
        return [card for card in self.decree.get(decree_option, []) if card not in self.decree_actions_taken.get(decree_option, [])]
    
    def take_decree_action(self, suit: Suit, decree_option: DecreeOption):
        # Try and find card of corresponding suit
        remaining_cards = self.get_remaining_decree(decree_option)
        for card in remaining_cards:
            if(card.suit == suit):
                self.decree_actions_taken.setdefault(decree_option, []).append(card)
                return
        
        # Default to using bird card if not found
        for card in remaining_cards:
            if(card.suit == Suit.Bird):
                self.decree_actions_taken.setdefault(decree_option, []).append(card)
                return
        
    def resolved_decree_option(self, decree_option: DecreeOption):
        if(len(self.decree.get(decree_option, [])) - len(self.decree_actions_taken.get(decree_option, [])) == 0):
            return True
        else:
            return False

    def suit_exists_in_decree_option(self, decree_option: DecreeOption, suit: Suit):
        remaining_cards = self.get_remaining_decree(decree_option)
        for card in remaining_cards:
            if(card.suit == suit or card.suit == Suit.Bird):
                return True
    
    def set_leader_viziers(self):
        for decree_option in LEADER_VIZIERS[self.leader]:
            self.decree.setdefault(decree_option, []).append(VizierCard())

    def turmoil(self):
        self.decree = {}
        self.decree_actions_taken = {}
        self.used_leaders.append(self.leader)

        if(len(self.used_leaders) == len(EyrieLeader)):
            self.used_leaders = []

        leader_options = [leader for leader in EyrieLeader if leader not in self.used_leaders]
        self.leader = random.choice(leader_options)
        self.set_leader_viziers()
    
    def reset_state(self):
        self.decree_actions_taken = {}

