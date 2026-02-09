from enum import Enum
from rootgame.engine.board import Board, Token, Building
from rootgame.engine.deck import Deck
from rootgame.engine.player import Player

from rootgame.engine.marquise_de_cat import MarquiseDeCat
from rootgame.engine.eyrie_dynasties import EyrieDynasties

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
    
    def is_action_legal(self, player: Player, action: str):
        if(action.startswith("MOVE")):
            if(len(action.split(" ")) != 4):
                return False
            
            numWarriors = int(action.split(" ")[1])
            startClearing = int(action.split(" ")[2])
            endClearing = int(action.split(" ")[3])

            if(not self.board.clearings[startClearing].isAdjacent(endClearing)):
                return False
            if(not self.board.clearings[endClearing].isAdjacent(startClearing)):
                return False
            if(self.board.clearings[startClearing].get_warrior_count(player.faction.faction_name) < numWarriors):
                return False
            return True
            
        elif action.startswith("PLAY CARD"):
            card_idx = int(action.split(" ")[2])
            if card_idx >= len(player.hand):
                return False
            return True
        
        elif action == "END PHASE":
            return True
        
        return False
            

    def apply_action(self, player: Player, action: str):
        # Check if is legal action
        if(not self.is_action_legal(player, action)):
            raise ValueError("Illegal Action Received")

        if action.startswith("MOVE"):
            numWarriors = int(action.split(" ")[1])
            startClearing = int(action.split(" ")[2])
            endClearing = int(action.split(" ")[3])
            self.move_warriors(player, numWarriors, startClearing, endClearing)

        elif action.startswith("PLAY CARD"):
            card_idx = action.split(" ")[2]
            self.play_card(player, int(card_idx))

        elif action == "END PHASE":
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

        return False
    
    def move_warriors(self, player: Player, numWarriors: int, startClearing: int, endClearing: int):
        self.board.clearings[startClearing].remove_warriors(player.faction.faction_name, numWarriors)
        self.board.clearings[endClearing].add_warriors(player.faction.faction_name, numWarriors)

    def play_card(self, player: Player, card_idx: int):
        card = player.hand[card_idx]
        player.hand.pop(card_idx)  # Remove the card from player's hand
        print(f"Playing card: {card.name}")
    
    def get_clearing_state(self):
        return self.board.export_clearing_info()
    
    def get_board_edges(self):
        return self.board.get_edges()