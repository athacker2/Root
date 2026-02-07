from dataclasses import dataclass
from rootgame.engine.types import Card
import random

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