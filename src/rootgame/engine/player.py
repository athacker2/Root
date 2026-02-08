from dataclasses import dataclass, field
from enum import Enum

class Character(Enum):
    NONE = 0
    MARQUISE_DE_CAT = 1
    EYRIE_DYNASTIES = 2
    WOODLAND_ALLIANCE = 3
    VAGABOND = 4


@dataclass
class Player:
    score: int = 0
    hand: list = field(default_factory=list)
    character: Character = Character.NONE