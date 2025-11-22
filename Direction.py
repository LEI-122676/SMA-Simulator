from enum import Enum


class Direction(Enum):  # Add more directions for more complex movement (more rays for the raycasting sensors)
    NORTH = (0, 1)
    SOUTH = (0, -1)
    WEST  = (-1, 0)
    EAST  = (1, 0)
