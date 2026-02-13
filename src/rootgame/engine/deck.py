from dataclasses import dataclass
import random

from rootgame.engine.card import Card
from rootgame.engine.base_deck import BASE_GAME_DECK

@dataclass
class Deck:
    cards: list[Card]

    def __init__(self):
        self.cards = BASE_GAME_DECK
        self.shuffle_deck()

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def draw_card(self, num_cards=1):
        if self.cards and len(self.cards) >= num_cards:
            return [self.cards.pop() for _ in range(num_cards)]
        else:
            raise IndexError("Deck is empty, cannot draw a card.")