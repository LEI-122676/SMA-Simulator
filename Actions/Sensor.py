from Actions.Direction import Direction
from Actions.Observation import Observation
from Items.ChickenCoop import ChickenCoop
from Items.Wall import Wall

class Sensor:

    def __init__(self, world_map, max_range: int = 10):
        self.world_map = world_map
        self.height = len(self.world_map)
        self.width = len(self.world_map[0])
        self.max_range = max_range

    def get_observation(self, explorer_id, explorer_position) -> Observation:
        observation = Observation(explorer_id)

        for direction in Direction:
            distance = self._cast_ray(explorer_position, direction.value)
            key_name = direction.name.title()  # 8 directions: "North", "NorthEast", "East"...

            # print("distance:", distance, "key_name:", key_name)      # Debug: Shows the distances for each direction

            if key_name in observation.possible_actions:
                observation.possible_actions[key_name] = distance

        return observation

    def _cast_ray(self, start_pos, step_vector) -> int:
        current_x, current_y = start_pos
        dx, dy = step_vector
        dist = 0

        for _ in range(self.max_range):
            current_x += dx
            current_y += dy

            # Check bounds
            if not (0 <= current_x < self.width and 0 <= current_y < self.height):
                return dist

            # Check for Wall
            if isinstance(self.world_map[current_y][current_x], Wall):
                return dist

            dist += 1

        return dist

    def get_coop_position(self):
        for y in range(self.height):
            for x in range(self.width):
                if isinstance(self.world_map[y][x], ChickenCoop):
                    return x, y

        return None