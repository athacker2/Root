from dataclasses import dataclass
from enum import Enum
from rootgame.engine.Board import Board
from rootgame.engine.Deck import Deck
from rootgame.engine.Player import Player

class TurnPhase(Enum):
    BIRDSONG = 1
    DAYLIGHT = 2
    EVENING = 3

class Game:
    players: list[Player]
    board: Board 
    deck: Deck
    current_phase: TurnPhase = TurnPhase.BIRDSONG
    turn: int = 0

    def __init__(self):
        # Initialize players, board, and game state
        self.players = [Player() for _ in range(2)]  # Assuming 2 players for now
        self.board = Board()

        self.deck = Deck()

        for player in self.players:
            player.score = 0  # Initialize player scores
            player.hand = self.deck.draw_card(5)  # Each player starts with 5 cards

    def get_legal_actions(self, player: Player):
        legal_actions = ["march", "end phase"]

        for card in player.hand:
            legal_actions.append(f"play card: {card.name}")
        
        return legal_actions

    def apply_action(self, player: Player, action: str):
        # Check if is legal action
        if(action not in self.get_legal_actions(player)):
            raise ValueError("Illegal Action Received")

        if action == "march":
            print("marching troops")
        elif action.startswith("play card"):
            card = action.split(": ")[1]
            player.hand = [c for c in player.hand if c.name != card]  # Remove the card from player's hand
            print(f"Playing card: {card}")
        elif action == "end phase":
            if(self.current_phase == TurnPhase.BIRDSONG):
                self.current_phase = TurnPhase.DAYLIGHT
                return False
            elif self.current_phase == TurnPhase.DAYLIGHT:
                self.current_phase = TurnPhase.EVENING
                return False
            elif self.current_phase == TurnPhase.EVENING:
                self.current_phase = TurnPhase.BIRDSONG
                self.turn += 1
                return True

        return False
    
    def get_clearing_state(self):
        return {clearing_id: "test" for clearing_id, _ in enumerate(self.board.clearings)}
    

