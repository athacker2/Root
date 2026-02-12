from enum import Enum, StrEnum, auto

class FactionName(StrEnum):
    NONE = auto()
    MARQUISE_DE_CAT = auto()
    EYRIE_DYNASTIES = auto()
    WOODLAND_ALLIANCE = auto()
    VAGABOND = auto()

class TurnPhase(Enum):
    BIRDSONG = 1
    DAYLIGHT = 2
    EVENING = 3

class Suit(StrEnum):
    Bird = auto()
    Fox = auto()
    Rabbit = auto()
    Mouse = auto()