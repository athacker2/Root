from dataclasses import dataclass, field
from enum import StrEnum, auto
from rootgame.engine.actions import Action, DiscardCardAction, DrawCardAction, EndPhaseAction, EyrieAddToDecreeAction, EyrieBattleAction, EyrieMoveAction, EyrieRecruitAction
from rootgame.engine.deck import Card
from rootgame.engine.faction import Faction
from rootgame.engine.board import Board
from rootgame.engine.building import BuildingType
from rootgame.engine.player import Player

from rootgame.engine.types import MAX_HAND_SIZE, FactionName, Suit, TurnPhase, DecreeOption

class Leader(StrEnum):
    DESPOT = auto()
    COMMANDER = auto()
    CHARISMATIC = auto()
    BUILDER = auto()

@dataclass
class EyrieDynasties(Faction):
    faction_name = FactionName.EYRIE_DYNASTIES

    leader: Leader | None = None

    decree: dict[DecreeOption, list[Card]] = field(default_factory=dict)
    decree_actions_taken: dict[DecreeOption, list[Card]] = field(default_factory=dict)

    def board_setup(self, board: Board):
        # Place roost in bottom right
        board.build(11, BuildingType.ROOST)

        # Place 6 warriors in starting clearing
        board.clearings[11].add_warriors(FactionName.EYRIE_DYNASTIES, 6)
    
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
            # If recruit actions left, must finish them
            if(len(self.decree.get(DecreeOption.Recruit, []))):
                if(isinstance(action, EyrieRecruitAction)):
                    if(not board.is_valid_clearing(action.clearing_id)):
                        return False
                    if(DecreeOption.Recruit not in self.decree or len(self.decree.get(DecreeOption.Recruit, [])) == 0):
                        return False
                    if(not board.clearings[action.clearing_id].suit in [card.suit for card in self.decree[DecreeOption.Recruit]]):
                        return False
                    if(not board.clearings[action.clearing_id].has_building(BuildingType.ROOST)):
                        return False
                    return True
                return False
            
            elif(len(self.decree.get(DecreeOption.Move, []))):
                if(isinstance(action, EyrieMoveAction)):
                    if(not board.can_move(self.faction_name, action.num_warriors, action.source_clearing, action.destination_clearing)):
                        return False
                    if(not board.clearings[action.source_clearing].suit in [card.suit for card in self.decree[DecreeOption.Move]]):
                        return False
                    return True
                return False
            
            elif(len(self.decree.get(DecreeOption.Battle, []))):
                if(isinstance(action, EyrieBattleAction)):
                    if(not board.can_battle(self.faction_name, action.defender.faction.faction_name, action.clearing_id)):
                        return False
                    if(not board.clearings[action.clearing_id].suit in [card.suit for card in self.decree[DecreeOption.Battle]]):
                        return False
                    return True
                return False
            
            elif(len(self.decree.get(DecreeOption.Build, []))):
                pass
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
                self.recruit(action.clearing_id, board)
                self.take_decree_action(board.clearings[action.clearing_id].suit, DecreeOption.Recruit)
            elif(isinstance(action, EyrieMoveAction)):
                board.move_warriors(self.faction_name, action.num_warriors, action.source_clearing, action.destination_clearing)
                self.take_decree_action(board.clearings[action.source_clearing].suit, DecreeOption.Move)
            elif(isinstance(action, EyrieBattleAction)):
                board.battle(self.faction_name, action.defender.faction.faction_name, action.clearing_id)
                self.take_decree_action(board.clearings[action.clearing_id].suit, DecreeOption.Battle)
                
    def add_to_decree(self, card: Card, decree_option: DecreeOption):
        if decree_option not in self.decree:
            self.decree[decree_option] = []
        self.decree[decree_option].append(card)
    
    def take_decree_action(self, suit: Suit, decree_option: DecreeOption):
        for (id, card) in enumerate(self.decree[decree_option]):
            if(card.suit == suit):
                used_card = self.decree[decree_option].pop(id)
                self.decree_actions_taken.setdefault(decree_option, []).append(used_card)
                break
                
    
    def recruit(self, clearing_id: int, board: Board):        
        board.clearings[clearing_id].add_warriors(FactionName.EYRIE_DYNASTIES, 1)