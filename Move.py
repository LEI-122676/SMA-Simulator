from enum import Enum
import random
from typing import Tuple
from Action import Action


class Move(Action, Enum):
    MOVE_NORTH = (0, 1)
    MOVE_SOUTH = (0, -1)
    MOVE_WEST  = (-1, 0)
    MOVE_EAST  = (1, 0)

    def to_tuple(self) -> Tuple[int, int]:
        return self.value

    @classmethod
    def random_action(cls) -> "Move":
        return random.choice(list(cls))
