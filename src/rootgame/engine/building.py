from dataclasses import dataclass
from enum import StrEnum, auto

from rootgame.engine.types import FactionName

class BuildingType(StrEnum):
    WORKSHOP = auto()
    SAWMILL = auto()
    RECRUITER = auto()
    ROOST = auto()

@dataclass
class Building():
    type: BuildingType
    used: bool = False
    owner: FactionName = None