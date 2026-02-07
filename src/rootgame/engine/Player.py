from dataclasses import dataclass, field

@dataclass
class Player:
    score: int = 0
    hand: list = field(default_factory=list)