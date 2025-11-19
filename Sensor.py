import numpy as np

from Action import Action
from Terrain import Terrain
from Wall import Wall


class Sensor:

    def __init__(self, terrain: Terrain, max_range:int = 10):
        self.grid = terrain.map
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.max_range = max_range

    def get_readings(self, agent_pos):
        readings = {}

        for direction in Action:                                        # ex: NORTH (0, 1)
            distance = self._cast_ray(agent_pos, direction.value)
            readings[direction] = distance

        return readings

    def _cast_ray(self, start_pos, step_vector):
        current_x, current_y = start_pos
        dx, dy = step_vector
        dist = 0

        # Continue stepping until we hit max range
        for _ in range(self.max_range):
            current_x += dx
            current_y += dy

            if not (0 <= current_x < self.width and 0 <= current_y < self.height):
                return dist

            if isinstance(self.grid[current_y][current_x], Wall):  # TODO - seria mais optimal usar numeros
                return dist

            dist += 1

        return dist

    def normalize_readings(self, readings):
        normalized = {}
        for direction, dist in readings.items():
            normalized[direction] = dist / self.max_range
        return normalized
