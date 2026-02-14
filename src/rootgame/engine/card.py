from dataclasses import dataclass, field
from typing import Protocol

from rootgame.engine.types import Suit

class Card(Protocol):
    suit: Suit | None = None

@dataclass
class EffectCard(Card):
    name: str
    persistent: bool
    suit: Suit | None = None
    crafting_requirements: list[Suit] = field(default_factory=list)

    def __repr__(self):
        return f"Effect: {self.suit.__str__()}, {[suit.__str__() for suit in self.crafting_requirements]}"

    def apply_effect(self):
        # Method that applies a card effect based on card's name
        pass

@dataclass
class ItemCard(Card):
    item: str
    crafting_VP: int
    suit: Suit | None = None
    crafting_requirements: dict[Suit, int] = field(default_factory=list)

    def __repr__(self):
        return f"Item: {self.suit.__str__()}, {[suit.__str__() for suit in self.crafting_requirements]}, {self.crafting_VP}"

@dataclass
class DominanceCard(Card):
    suit: Suit | None = None

    def __repr__(self):
        return f"Dominance: {self.suit.__str__()}"

@dataclass
class AmbushCard(Card):
    suit: Suit | None = None

    def __repr__(self):
        return f"Ambush: {self.suit.__str__()}"

@dataclass
class VizierCard(Card):
    name: str = "Vizier"
    suit: Suit = Suit.Bird

    