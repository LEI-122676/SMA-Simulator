import numpy as np
from NeuralNetworks.NeuralNetwork import NeuralNetwork


class NeuralNetworkForaging(NeuralNetwork):
    """
    Inputs (13 total):
    - 8 raycast directions (normalized distances to obstacles)
    - 1 inventory flag (1.0 if carrying egg, 0.0 if not)
    - 2 target direction (dx, dy to nearest egg or nest, normalized)
    - 2 target distance (distance to nearest egg and nearest available nest, normalized)
    """

    INPUT_SIZE = 13

    def __init__(self, hidden_architecture, hidden_activation, output_activation):
        super().__init__(self.INPUT_SIZE, hidden_architecture, hidden_activation, output_activation)

    def get_input_size(self):
        return self.INPUT_SIZE

def create_foraging_network():
    hidden_architecture = (4,)
    hidden_fn = lambda x: 1 / (1 + np.exp(-x))
    output_fn = lambda x: np.tanh(x)

    return NeuralNetworkForaging(hidden_architecture, hidden_fn, output_fn)