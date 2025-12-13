import numpy as np

from NeuralNetworks.NeuralNetwork import NeuralNetwork


class NeuralNetworkCoop(NeuralNetwork):
    """
    Inputs (11 total):
    - 8 raycast directions (normalized distances to obstacles)
    - 2 coop vector (dx, dy normalized direction to coop)
    """

    INPUT_SIZE = 10

    def __init__(self, hidden_architecture, hidden_activation, output_activation):
        super().__init__(self.INPUT_SIZE, hidden_architecture, hidden_activation, output_activation)

    def get_input_size(self):
        return self.INPUT_SIZE

def create_coop_network():
    hidden_architecture = (4,)
    hidden_fn = lambda x: 1 / (1 + np.exp(-x))
    # Map to continuous range [-1, 1] instead of binary [1, -1]
    output_fn = lambda x: np.tanh(x)

    return NeuralNetworkCoop(hidden_architecture, hidden_fn, output_fn)