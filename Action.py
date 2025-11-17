from enum import Enum
import random

class Action(Enum):
    # Name     = Value
    MOVE_NORTH = (0, 1)
    MOVE_SOUTH = (0, -1)
    MOVE_WEST  = (-1, 0)
    MOVE_EAST  = (1, 0)

    @classmethod
    def random_action(cls):
        return random.choice(list(cls)).value

# --- Usage ---
# print(list(Action))          # Automatic list of all actions
# print(Action.MOVE_NORTH)     # Prints: Action.MOVE_NORTH
# print(Action.MOVE_NORTH.value) # Prints: (0, 1)
# print(Action.MOVE_NORTH.name)  # Prints: "MOVE_NORTH"

