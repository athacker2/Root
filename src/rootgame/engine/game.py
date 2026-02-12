import random

from rootgame.engine.game_log import GameLog
from rootgame.engine.board import Board
from rootgame.engine.deck import Deck
from rootgame.engine.player import Player

from rootgame.engine.marquise_de_cat import MarquiseDeCat
from rootgame.engine.eyrie_dynasties import EyrieDynasties

from rootgame.engine.actions import *

from rootgame.engine.types import TurnPhase, EyrieLeader

class Game:
    players: list[Player]
    board: Board
    deck: Deck

    game_log: GameLog

    # Turn-related data
    round: int = 0
    current_player: int = 0
    current_phase: TurnPhase = TurnPhase.BIRDSONG

    def __init__(self):
        # Initialize players, board, and game state
        self.players = [Player() for _ in range(2)]  # Assuming 2 players for now
        self.players[0].faction = EyrieDynasties(EyrieLeader.BUILDER)
        self.players[1].faction = MarquiseDeCat()

        self.deck = Deck()
        for player in self.players:
            player.hand = self.deck.draw_card(5)  # Each player starts with 5 cards

        self.board = Board()
        self.new_game_board_setup()

        self.game_log = GameLog()

    def new_game_board_setup(self):
        for p in self.players:
            p.faction.board_setup(self.board)

    def get_legal_actions(self, player: Player):
        return player.faction.get_legal_actions(self.current_phase, self.board)
    
    def is_action_legal(self, player: Player, action: Action):
        return player.faction.is_action_legal(action, self.current_phase, player, self.board, self.game_log.get_actions_for_turn_phase(self.round, self.current_phase))
            
    def apply_action(self, player: Player, action: Action):
        # Check if is legal action
        if(not self.is_action_legal(player, action)):
            raise ValueError("Illegal Action Received")
        elif isinstance(action, EndPhaseAction):
            if(self.current_phase == TurnPhase.BIRDSONG):
                self.current_phase = TurnPhase.DAYLIGHT
                return False
            elif self.current_phase == TurnPhase.DAYLIGHT:
                self.current_phase = TurnPhase.EVENING
                return False
            elif self.current_phase == TurnPhase.EVENING:
                self.current_phase = TurnPhase.BIRDSONG

                # Mark all buildings as unused at the end of the round
                self.board.mark_all_buildings_unused()
                player.faction.reset_state()
                self.round += 1
        else:
            player.faction.apply_action(action, self.board, player)
        
        self.game_log.log_action(self.round, player, self.current_phase, action)

    def play_card(self, player: Player, card_idx: int):
        card = player.hand[card_idx]
        player.hand.pop(card_idx)  # Remove the card from player's hand
        print(f"Playing card: {card.name}")

    def get_clearing_state(self):
        return self.board.export_clearing_info()
    
    def get_board_edges(self):
        return self.board.get_edges()