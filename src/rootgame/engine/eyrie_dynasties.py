from dataclasses import dataclass, field
from enum import StrEnum, auto
from rootgame.engine.actions import Action, DiscardCardAction, DrawCardAction, EndPhaseAction, EyrieAddToDecreeAction
from rootgame.engine.deck import Card
from rootgame.engine.faction import Faction
from rootgame.engine.board import Board
from rootgame.engine.building import BuildingType
from rootgame.engine.player import Player

from rootgame.engine.types import MAX_HAND_SIZE, FactionName, TurnPhase, DecreeOption

class Leader(StrEnum):
    DESPOT = auto()
    COMMANDER = auto()
    CHARISMATIC = auto()
    BUILDER = auto()

@dataclass
class EyrieDynasties(Faction):
    faction_name = FactionName.EYRIE_DYNASTIES
    decree: map[DecreeOption, list[Card]] = field(default_factory=dict)
    leader: Leader | None = None

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
            # Check if action is "RECRUIT", "MOVE", "BATTLE", or "BUILD" and if the player can perform the action
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
        
        return False
    
    def apply_action(self, action: Action, board: Board, player: Player):
            if(isinstance(action, EyrieAddToDecreeAction)):
                card = player.hand[action.card_id]
                self.add_to_decree(card, action.decree_option)
                player.hand.pop(action.card_id)
                
    def add_to_decree(self, card: Card, option: DecreeOption):
        if option not in self.decree:
            self.decree[option] = []
        self.decree[option].append(card)