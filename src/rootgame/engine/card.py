from dataclasses import dataclass, field
from typing import Protocol

from rootgame.engine.types import Suit

class Card(Protocol):
    suit: Suit | None = None

@dataclass
class EffectCard(Card):
    name: str
    suit: Suit | None = None
    persistent: bool
    crafting_requirements: list[Suit] = field(default_factory=list)

    def apply_effect(self):
        # Method that applies a card effect based on card's name
        pass

@dataclass
class ItemCard(Card):
    item: str
    suit: Suit | None = None
    crafting_requirements: list[Suit] = field(default_factory=list)
    crafting_VP: int

@dataclass
class DominanceCard(Card):
    suit: Suit | None = None

@dataclass
class AmbushCard(Card):
    suit: Suit | None = None
    