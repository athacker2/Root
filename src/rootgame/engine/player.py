from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Player:
    score: int = 0
    hand: list = field(default_factory=list)
    faction: Optional["Faction"] = None