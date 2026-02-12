from dataclasses import dataclass, field

from build.lib.rootgame.engine.player import Player
from rootgame.engine.actions import Action
from rootgame.engine.types import TurnPhase

@dataclass
class GameLog:
    actions_taken: list[tuple[Player, dict[TurnPhase, list[Action]]]] = field(default_factory=list)

    def log_action(self, turn: int, player: Player, phase: TurnPhase, action: Action):
        if(len(self.actions_taken) <= turn):
            self.actions_taken.append((player, {phase: [action]}))
        else:
            if phase not in self.actions_taken[turn][1]:
                self.actions_taken[turn][1][phase] = []
            self.actions_taken[turn][1][phase].append(action)
        
    def get_actions_for_turn_phase(self, turn: int, phase: TurnPhase):
        if(turn < len(self.actions_taken)):
            return self.actions_taken[turn][1].get(phase, [])
        else:
            return []