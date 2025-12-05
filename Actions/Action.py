from enum import Enum
import random

class Action(Enum):

    MOVE_NORTH = (0, 1)
    MOVE_SOUTH = (0, -1)
    MOVE_WEST  = (-1, 0)
    MOVE_EAST  = (1, 0)

    @classmethod
    def random_action(cls):
        return random.choice(list(cls))

    @classmethod
    def get_all_actions(cls):
        return list(Action)