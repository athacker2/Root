from dataclasses import dataclass, field
from typing import Optional
from rootgame.engine.card import Card

@dataclass
class Player:
    score: int = 0
    hand: list[Card] = field(default_factory=list)
    faction: Optional["Faction"] = None