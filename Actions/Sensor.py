from Actions.Direction import Direction
from Actions.Observation import Observation
from Items.ChickenCoop import ChickenCoop
from Items.Wall import Wall
from Items.Egg import Egg
from Items.Nest import Nest
from Items.Stone import Stone


class Sensor:

    def __init__(self, world_map, max_range: int = 10):
        self.world_map = world_map
        self.height = len(self.world_map)
        self.width = len(self.world_map[0])
        self.max_range = max_range
        self.coop_position = self._get_coop_position()

    def get_observation(self, explorer_position) -> Observation:
        observation = Observation()

        for direction in Direction:
            # Returns (dist, obj_instance)
            distance, obj_hit = self._cast_ray(explorer_position, direction.value)

            key_name = direction.name.title()
            # Store Type (Class) for generic identification
            obj_type = type(obj_hit) if obj_hit is not None else None

            observation.add_ray(key_name, distance, obj_type)

        return observation

    def _cast_ray(self, start_pos, step_vector):
        """ Returns (distance, object_hit) """
        current_x, current_y = start_pos
        dx, dy = step_vector
        dist = 0

        for _ in range(self.max_range):
            current_x += dx
            current_y += dy

            # Check bounds (World Edge acts as a Wall)
            if not (0 <= current_x < self.width and 0 <= current_y < self.height):
                # Return a Wall instance with dummy ID and coordinates
                return dist, Wall(0, current_x, current_y)

            obj = self.world_map[current_y][current_x]

            # Stop at physical objects
            if isinstance(obj, (Wall, ChickenCoop, Nest, Stone, Egg)):
                return dist, obj

            dist += 1

        return dist, None

    def _get_coop_position(self):
        for y in range(self.height):
            for x in range(self.width):
                if isinstance(self.world_map[y][x], ChickenCoop):
                    return x, y
        return None, None

    def get_goal_vector(self, explorer_position):
        if self.coop_position == (None, None):
            return None

        coop_x, coop_y = self.coop_position
        agent_x, agent_y = explorer_position

        return coop_x - agent_x, coop_y - agent_y