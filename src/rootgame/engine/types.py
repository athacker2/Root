from dataclasses import dataclass, field
import random

@dataclass
class Card:
    name: str
    suit: str
    value: int

@dataclass
class Deck:
    cards: list[Card]

    def initialize_deck(self):
        # Initialize the deck with cards
        suits = ['Bird', 'Fox', 'Rabbit', 'Mouse']
        for suit in suits:
            for value in range(1, 14):
                card_name = f"{suit.capitalize()} {value}"
                self.cards.append(Card(name=card_name, suit=suit, value=value))
    
    def shuffle_deck(self):
        random.shuffle(self.cards)

    def draw_card(self, num_cards=1):
        if self.cards:
            return [self.cards.pop() for _ in range(num_cards)]
        else:
            raise IndexError("Deck is empty, cannot draw a card.")

@dataclass
class Player:
    score: int = 0
    hand: list[Card] = None

@dataclass
class Clearing:
    adjacentClearings: list[int] = field(default_factory=list)
    tiles: list[str] = field(default_factory=list)
    suit: str = ""

@dataclass
class Board:
    clearings: list[Clearing]

@dataclass
class GameState:
    players: list[Player]
    board: Board 
    deck: Deck
    turn: int = 0