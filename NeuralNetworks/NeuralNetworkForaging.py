import numpy as np
import math
from NeuralNetworks.NeuralNetwork import NeuralNetwork
from Items.Wall import Wall
from Items.Egg import Egg
from Items.Nest import Nest
from Items.Stone import Stone


class NeuralNetworkForaging(NeuralNetwork):
    """
    Inputs (19 total):
    - 8 raycast distances
    - 8 raycast object types
    - 1 inventory flag
    - 2 nearest target vector
    """

    INPUT_SIZE = 19

    def __init__(self, hidden_architecture, hidden_activation, output_activation):
        super().__init__(self.INPUT_SIZE, hidden_architecture, hidden_activation, output_activation)

    def get_input_size(self):
        return self.INPUT_SIZE

    def get_inputs(self, agent) -> list:
        inputs = []

        # 1. Raycast Data (16 inputs)
        has_item = len(agent.inventory) > 0
        max_range = agent.sensor.max_range
        directions = ["North", "NorthEast", "East", "SouthEast",
                      "South", "SouthWest", "West", "NorthWest"]

        for direction in directions:
            # Use .rays access as established
            dist, obj_type = agent.observation.rays.get(direction, (0, None))
            inputs.append(dist / max_range if max_range > 0 else 0)

            type_val = 0.0
            if obj_type == Wall:
                type_val = -1.0
            elif obj_type == Stone:
                type_val = -0.5
            elif obj_type == Egg:
                type_val = 0.5 if not has_item else 0.0
            elif obj_type == Nest:
                type_val = 0.5 if has_item else 0.0

            inputs.append(type_val)

        # 2. Inventory (1 input)
        inputs.append(1.0 if has_item else 0.0)

        # 3. Vector to Nearest Relevant Target (2 inputs)
        target = None
        if has_item:
            target = self._get_nearest(agent, agent.world.nests)
        else:
            available_eggs = [e for e in agent.world.eggs if not e.picked_up]
            target = self._get_nearest(agent, available_eggs)

        if target:
            tx = target.position[0] - agent.position[0]
            ty = target.position[1] - agent.position[1]

            # --- IMPROVEMENT: Separate Normalization ---
            w = agent.world.width if agent.world else 30
            h = agent.world.height if agent.world else 30

            inputs.append(tx / w)
            inputs.append(ty / h)
        else:
            inputs.extend([0.0, 0.0])

        return inputs

    def _get_nearest(self, agent, objects):
        if not objects: return None
        return min(objects, key=lambda o: math.dist(agent.position, o.position))


# --- FACTORY FUNCTION ---
def create_foraging_network():
    hidden_architecture = (8, 6)
    hidden_fn = lambda x: np.maximum(0, x)
    output_fn = lambda x: np.tanh(x)

    return NeuralNetworkForaging(hidden_architecture, hidden_fn, output_fn)