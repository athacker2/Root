from dataclasses import dataclass
import random

from rootgame.engine.types import Suit

@dataclass
class Card:
    name: str
    suit: Suit
    value: int

@dataclass
class Deck:
    cards: list[Card]

    def __init__(self):
        self.cards = []

        # Initialize the deck with cards
        for suit in Suit:
            for value in range(1, 4):
                card_name = f"{suit.capitalize()} {value}"
                self.cards.append(Card(name=card_name, suit=suit, value=value))
        
        self.shuffle_deck()

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def draw_card(self, num_cards=1):
        if self.cards and len(self.cards) >= num_cards:
            return [self.cards.pop() for _ in range(num_cards)]
        else:
            raise IndexError("Deck is empty, cannot draw a card.")