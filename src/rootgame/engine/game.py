from dataclasses import dataclass
from enum import Enum
from rootgame.engine.board import Board, Token, Building
from rootgame.engine.deck import Deck
from rootgame.engine.player import Player, Character

class TurnPhase(Enum):
    BIRDSONG = 1
    DAYLIGHT = 2
    EVENING = 3

@dataclass
class Game:
    players: list[Player]
    board: Board 
    deck: Deck
    current_phase: TurnPhase = TurnPhase.BIRDSONG
    turn: int = 0

    def __init__(self):
        # Initialize players, board, and game state
        self.players = [Player() for _ in range(2)]  # Assuming 2 players for now
        self.players[0].character = Character.MARQUISE_DE_CAT
        self.players[1].character = Character.EYRIE_DYNASTIES

        self.deck = Deck()

        self.board = Board()
        self.new_game_board_setup()


        for player in self.players:
            player.score = 0  # Initialize player scores
            player.hand = self.deck.draw_card(5)  # Each player starts with 5 cards

    def new_game_board_setup(self):
        for p in self.players:
            if p.character == Character.MARQUISE_DE_CAT:
                self.marquise_de_cat_setup()
            elif p.character == Character.EYRIE_DYNASTIES:
                self.eyrie_dynasties_setup()
            elif p.character == Character.WOODLAND_ALLIANCE:
                self.woodland_alliance_setup()
            elif p.character == Character.VAGABOND:
                self.vagabond_setup()

    def marquise_de_cat_setup(self):
        # Place keep in top left clearing (TO CHANGE W/INTERACTIVE SETUP)
        self.board.clearings[0].add_token(Character.MARQUISE_DE_CAT, Token.KEEP)

        # Place one of each building in clearings adjacent to keep
        self.board.clearings[4].add_building(Building.WORKSHOP)
        self.board.clearings[3].add_building(Building.SAWMILL)
        self.board.clearings[1].add_building(Building.RECRUITER)

        # Place 1 warrior in every clearing (except corner opposite to keep)
        for (id, clearing) in enumerate(self.board.clearings):
            if id != 11:
                clearing.add_warrior(Character.MARQUISE_DE_CAT, 1)
    
    def eyrie_dynasties_setup(self):
        # Place roost in bottom right
        self.board.clearings[11].add_building(Building.ROOST)

        # Place 6 warriors in starting clearing
        self.board.clearings[11].add_warrior(Character.EYRIE_DYNASTIES, 6)
    
    def woodland_alliance_setup(self):
        return
    
    def vagabond_setup(self):
        return

    def get_legal_actions(self, player: Player):
        legal_actions = ["MOVE", "END PHASE", "PLAY CARD"]
        return legal_actions
    
    def is_action_legal(self, player: Player, action: str):
        if(action.startswith("MOVE")):
            if(len(action.split(" ")) != 4):
                return False
            
            numWarriors = int(action.split(" ")[1])
            startClearing = int(action.split(" ")[2])
            endClearing = int(action.split(" ")[3])

            if(startClearing not in self.board.clearings[endClearing].adjacentClearings):
                return False
            if(endClearing not in self.board.clearings[startClearing].adjacentClearings):
                return False
            if(self.board.clearings[startClearing].warriors[player.character] < numWarriors):
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
                self.turn += 1
                return True

        return False
    
    def move_warriors(self, player: Player, numWarriors: int, startClearing: int, endClearing: int):
        self.board.clearings[startClearing].warriors[player.character] -= numWarriors
        self.board.clearings[endClearing].warriors[player.character] = self.board.clearings[endClearing].warriors.get(player.character, 0) + numWarriors

    def play_card(self, player: Player, card_idx: int):
        card = player.hand[card_idx]
        player.hand.pop(card_idx)  # Remove the card from player's hand
        print(f"Playing card: {card.name}")
    
    def get_clearing_state(self):
        return self.board.export_clearing_info()
    

