from dataclasses import dataclass

@dataclass
class Player:
    score: int = 0

@dataclass
class Clearing:
    adjacentClearings: list[int]
    tiles: list[str]
    suit: str | None

@dataclass
class Board:
    clearings: list[Clearing]

@dataclass
class GameState:
    players: list[Player]
    board: Board | None
    turn: int = 0

@dataclass
class Card:
    name: str
    suit: str
    value: int