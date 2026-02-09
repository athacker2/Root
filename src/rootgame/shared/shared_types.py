from dataclasses import dataclass, field

@dataclass
class ClearingInfo:
    tiles: list[str] = field(default_factory=list)
    warriors: dict[str, int] = field(default_factory=dict)
    tokens: dict[str, list[str]] = field(default_factory=dict)
    suit: str = ""