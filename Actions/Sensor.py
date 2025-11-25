from Actions.Direction import Direction
from Agent.ExplorerAgent import ExplorerAgent
from Observation import Observation
from Obstacle.Obstacle import Obstacle
from World.World import World


class Sensor: # uses raycasting to detect distances to obstacles

    def __init__(self, world: World, max_range:int = 10):
        self.world = world
        self.height = len(self.world.map)
        self.width = len(self.world.map[0])
        self.max_range = max_range

    def get_observation(self, explorer: ExplorerAgent) -> Observation:
        observation = Observation(explorer.id)

        for direction in Direction:                                        # ex: NORTH (0, 1)
            distance = self._cast_ray(explorer.position, direction.value)
            observation.possible_actions[direction] = distance

        return observation

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

            if isinstance(self.world.map[current_y][current_x], Obstacle):
                return dist

            dist += 1

        return dist
