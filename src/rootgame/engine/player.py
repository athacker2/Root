from dataclasses import dataclass, field
from enum import StrEnum, auto

class Character(StrEnum):
    NONE = auto()
    MARQUISE_DE_CAT = auto()
    EYRIE_DYNASTIES = auto()
    WOODLAND_ALLIANCE = auto()
    VAGABOND = auto()


@dataclass
class Player:
    score: int = 0
    hand: list = field(default_factory=list)
    character: Character = Character.NONE