from enum import Enum


class Direction(Enum):  # Add more directions for more complex movement (more rays for the raycasting sensors)
    NORTH = (0, 1)
    SOUTH = (0, -1)
    WEST  = (1, 0)
    EAST  = (-1, 0)

    NORTH_EAST = (-1, 1)
    NORTH_WEST = (1, 1)
    SOUTH_EAST = (-1, -1)
    SOUTH_WEST = (1, -1)