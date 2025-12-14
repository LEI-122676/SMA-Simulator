import numpy as np
from NeuralNetworks.NeuralNetwork import NeuralNetwork
from Items.ChickenCoop import ChickenCoop
from Items.Wall import Wall


class NeuralNetworkCoop(NeuralNetwork):
    """
    Inputs (18 total):
    - 8 raycast distances (normalized)
    - 8 raycast object types (encoded)
    - 2 coop vector (dx, dy normalized separately)
    """

    INPUT_SIZE = 18

    def __init__(self, hidden_architecture, hidden_activation, output_activation):
        super().__init__(self.INPUT_SIZE, hidden_architecture, hidden_activation, output_activation)

    def get_input_size(self):
        return self.INPUT_SIZE

    def get_inputs(self, agent) -> list:
        inputs = []

        # 1. Raycast Data (16 inputs)
        max_range = agent.sensor.max_range
        directions = ["North", "NorthEast", "East", "SouthEast",
                      "South", "SouthWest", "West", "NorthWest"]

        for direction in directions:
            dist, obj_type = agent.observation.rays.get(direction, (0, None))

            norm_dist = dist / max_range if max_range > 0 else 0
            inputs.append(norm_dist)

            type_val = 0.0
            if obj_type == Wall:
                type_val = -1.0
            elif obj_type == ChickenCoop:
                type_val = 1.0
            inputs.append(type_val)

        # 2. Goal Vector (2 inputs)
        if agent.goal_vector is not None:
            dx, dy = agent.goal_vector

            # --- IMPROVEMENT: Separate Normalization for X and Y ---
            # This preserves the true angle better than using a single max dimension
            w = agent.world.width if agent.world else 30
            h = agent.world.height if agent.world else 30

            inputs.append(dx / w)
            inputs.append(dy / h)
        else:
            inputs.extend([0.0, 0.0])

        return inputs


def create_coop_network():
    hidden_architecture = (6,)

    # Activation Functions
    hidden_fn = lambda x: np.maximum(0, x)  # ReLU
    output_fn = lambda x: np.tanh(x)  # Tanh (-1 to 1)

    return NeuralNetworkCoop(hidden_architecture, hidden_fn, output_fn)