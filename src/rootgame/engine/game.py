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
    current_player: Player | None = None
    current_phase: TurnPhase = TurnPhase.BIRDSONG

    def __init__(self):
        # Initialize players, board, and game state
        self.players = [Player() for _ in range(2)]  # Assuming 2 players for now
        self.players[1].faction = EyrieDynasties(EyrieLeader.BUILDER)
        self.players[0].faction = MarquiseDeCat()

        self.current_player = self.players[0]

        self.deck = Deck()
        for player in self.players:
            player.hand = self.deck.draw_card(3)  # Each player starts with 3 cards

        self.board = Board()
        self.new_game_board_setup()

        self.game_log = GameLog()

        # Do pre-birdsong actions for new player
        actions_to_run = self.current_player.faction.pre_birdsong_actions()
        for action in actions_to_run:
            self.apply_action(action)

    def new_game_board_setup(self):
        for p in self.players:
            p.faction.board_setup(self.board)

    def get_legal_actions(self):
        return self.current_player.faction.get_legal_actions(self.current_phase)
    
    def is_action_legal(self, action: Action):
        return self.current_player.faction.is_action_legal(action, self.current_phase, self.current_player, self.board, self.game_log.get_actions_for_turn_phase(self.round, self.current_phase))
            
    def apply_action(self, action: Action):
        # Log the action
        self.game_log.log_action(self.round, self.current_player, self.current_phase, action)

        if isinstance(action, EndPhaseAction):
            if(self.current_phase == TurnPhase.BIRDSONG):
                self.current_phase = TurnPhase.DAYLIGHT

            elif self.current_phase == TurnPhase.DAYLIGHT:
                # Do pre-evening actions
                actions_to_run = self.current_player.faction.pre_evening_actions()
                for action in actions_to_run:
                    self.apply_action(action)

                self.current_phase = TurnPhase.EVENING

            elif self.current_phase == TurnPhase.EVENING:
                # Do end of turn clean up for player
                self.board.mark_all_buildings_unused()
                self.current_player.faction.reset_state()

                # Move to next round/phase
                self.round += 1
                self.current_phase = TurnPhase.BIRDSONG
                self.current_player = self.players[self.round % len(self.players)]

                # Do pre-birdsong actions for next player
                actions_to_run = self.current_player.faction.pre_birdsong_actions()
                for action in actions_to_run:
                    self.apply_action(action)

        elif(isinstance(action, DrawCardAction)):
            self.current_player.hand.extend(self.deck.draw_card(action.num_cards))
        elif(isinstance(action, DiscardCardAction)):
            self.discard_cards(self.current_player, action.card_ids)
        else:
            self.current_player.faction.apply_action(action, self.board, self.current_player)

    def play_card(self, player: Player, card_idx: int):
        card = player.hand[card_idx]
        player.hand.pop(card_idx)  # Remove the card from player's hand
        print(f"Playing card: {card.suit}")
    
    def discard_cards(self, player: Player, cards: list[int]):
        new_hand = list()
        for (id, card) in enumerate(player.hand):
            if(not id in cards):
                new_hand.append(card)
        player.hand = new_hand

    def get_clearing_state(self):
        return self.board.export_clearing_info()
    
    def get_board_edges(self):
        return self.board.get_edges()