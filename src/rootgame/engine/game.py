import random

from rootgame.engine.board import Board
from rootgame.engine.deck import Deck
from rootgame.engine.player import Player

from rootgame.engine.marquise_de_cat import MarquiseDeCat
from rootgame.engine.eyrie_dynasties import EyrieDynasties

from rootgame.engine.actions import *

from rootgame.engine.types import TurnPhase

class Game:
    players: list[Player]
    board: Board
    deck: Deck

    # Turn-related data
    round: int = 0
    current_player: int = 0
    current_phase: TurnPhase = TurnPhase.BIRDSONG

    def __init__(self):
        # Initialize players, board, and game state
        self.players = [Player() for _ in range(2)]  # Assuming 2 players for now
        self.players[0].faction = MarquiseDeCat()
        self.players[1].faction = EyrieDynasties()

        self.deck = Deck()
        for player in self.players:
            player.hand = self.deck.draw_card(5)  # Each player starts with 5 cards

        self.board = Board()
        self.new_game_board_setup()

    def new_game_board_setup(self):
        for p in self.players:
            p.faction.board_setup(self.board)

    def get_legal_actions(self, player: Player):
        return player.faction.get_legal_actions(self.current_phase)
    
    def is_action_legal(self, player: Player, action: Action):
        if(isinstance(action, MoveAction)):
            num_warriors = action.num_warriors
            source_clearing = action.source_clearing
            destination_clearing = action.destination_clearing

            if(source_clearing >= len(self.board.clearings) or destination_clearing >= len(self.board.clearings)):
                return False
            if(source_clearing == destination_clearing):
                return False
            if(not self.board.clearings[source_clearing].is_adjacent(destination_clearing)):
                return False
            if(not self.board.clearings[destination_clearing].is_adjacent(source_clearing)):
                return False
            if(self.board.clearings[source_clearing].get_warrior_count(player.faction.faction_name) < num_warriors):
                return False

            return True
        
        elif isinstance(action, BattleAction):
            clearing_id = action.clearing_id
            attacker = action.attacker
            defender = action.defender

            if(clearing_id >= len(self.board.clearings)):
                return False
            if(attacker == defender):
                return False
            if(self.board.clearings[clearing_id].get_warrior_count(attacker.faction.faction_name) == 0):
                return False
            if(self.board.clearings[clearing_id].get_warrior_count(defender.faction.faction_name) == 0):
                return False
            
            return True
            
        elif isinstance(action, PlayCardAction):
            card_id = action.card_id
            if card_id >= len(player.hand):
                return False
            return True
        
        elif isinstance(action, RecruitAction):
            clearing_id = action.clearing_id
            if(clearing_id >= len(self.board.clearings)):
                return False
            return True
        
        elif isinstance(action, EndPhaseAction):
            return True
        
        elif(isinstance(player.faction, MarquiseDeCat)):
            return player.faction.is_action_legal(action, self.current_phase, player, self.board)
        
        return False
            
    def apply_action(self, player: Player, action: Action):
        # Check if is legal action
        if(not self.is_action_legal(player, action)):
            raise ValueError("Illegal Action Received")

        if isinstance(action, MoveAction):
            num_warriors = action.num_warriors
            source_clearing = action.source_clearing
            destination_clearing = action.destination_clearing
            self.board.move_warriors(player.faction.faction_name, num_warriors, source_clearing, destination_clearing)

        elif isinstance(action, PlayCardAction):
            card_id = action.card_id
            self.play_card(player, card_id)

        elif isinstance(action, BattleAction):
            clearing_id = action.clearing_id
            defender = action.defender
            attacker = action.attacker
            self.battle(attacker, defender, clearing_id)

        elif isinstance(action, EndPhaseAction):
            if(self.current_phase == TurnPhase.BIRDSONG):
                self.current_phase = TurnPhase.DAYLIGHT
                return False
            elif self.current_phase == TurnPhase.DAYLIGHT:
                self.current_phase = TurnPhase.EVENING
                return False
            elif self.current_phase == TurnPhase.EVENING:
                self.current_phase = TurnPhase.BIRDSONG
                self.round += 1
                return True
        
        elif isinstance(action, AddWoodToSawmillsAction):
            if(isinstance(player.faction, MarquiseDeCat)):
                player.faction.add_wood_to_sawmills(self.board)
        
        elif isinstance(action, MarchAction):
            if(isinstance(player.faction, MarquiseDeCat)):
                player.faction.march(self.board, action.move_one.num_warriors, action.move_one.source_clearing, action.move_one.destination_clearing,
                                     action.move_two.num_warriors, action.move_two.source_clearing, action.move_two.destination_clearing)
        elif(isinstance(action, MarquiseRecruitAction)):
            if(isinstance(player.faction, MarquiseDeCat)):
                player.faction.recruit(self.board)
            
        elif(isinstance(action, MarquiseBuildAction)):
            if(isinstance(player.faction, MarquiseDeCat)):
                player.faction.build(self.board, action.clearing_id, action.building)

        return False

    def play_card(self, player: Player, card_idx: int):
        card = player.hand[card_idx]
        player.hand.pop(card_idx)  # Remove the card from player's hand
        print(f"Playing card: {card.name}")
    
    def battle(self, attacker: Player, defender: Player, clearing_id: int):
        battle_clearing = self.board.clearings[clearing_id]
        rolls = [random.randint(0, 3) for _ in range(2)]

        attack_hits = min(max(rolls), battle_clearing.get_warrior_count(attacker.faction.faction_name))
        defense_hits = min(min(rolls), battle_clearing.get_warrior_count(defender.faction.faction_name))

        battle_clearing.remove_warriors(attacker.faction.faction_name, defense_hits)
        battle_clearing.remove_warriors(defender.faction.faction_name, attack_hits)



    def get_clearing_state(self):
        return self.board.export_clearing_info()
    
    def get_board_edges(self):
        return self.board.get_edges()