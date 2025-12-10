import numpy as np


class NeuralNetwork:

    def __init__(self, input_size, hidden_architecture, hidden_activation, output_activation):
        self.input_size = input_size #dado pelo sensor?
        self.hidden_architecture = hidden_architecture #tuple with the number of neurons in each hidden layer: (5, 2)-> 2 hidden layers, 1st has 5n and 2nd has 2n
        # The activations are functions
        self.hidden_activation = hidden_activation
        self.output_activation = output_activation

    def compute_num_weights(self):
        total = 0
        input_size = self.input_size
        for n in self.hidden_architecture:
            total += (input_size + 1) * n
            input_size = n
        total += (input_size + 1) * 4  # 4 neurons for N, S, E, W
        return total

    def load_weights(self, weights):
        w = np.array(weights)
        self.hidden_weights = []
        self.hidden_biases = []
        start_w = 0
        input_size = self.input_size
        for n in self.hidden_architecture:
            end_w = start_w + (input_size * n)
            self.hidden_weights.append(w[start_w:end_w].reshape(input_size, n))
            start_w = end_w
            self.hidden_biases.append(w[start_w:start_w + n])
            start_w += n
            input_size = n
        # Final Layer (4 neurons)
        end_w = start_w + (input_size * 4)
        self.output_weights = w[start_w:end_w].reshape(input_size, 4)
        self.output_bias = w[end_w:]

    def forward(self, x):
        a = np.array(x)
        for i in range(len(self.hidden_architecture)):
            z = np.dot(a, self.hidden_weights[i]) + self.hidden_biases[i]
            a = self.hidden_activation(z)
        return np.dot(a, self.output_weights) + self.output_bias  # Returns 4 values


def create_network_architecture(input_size):
    hidden_architecture = (3,)
    hidden_fn = lambda x: 1 / (1 + np.exp(-x))

    # Map to continuous range [-1, 1] instead of binary [1, -1]
    output_fn = lambda x: np.tanh(x)
    return NeuralNetwork(input_size, hidden_architecture, hidden_fn, output_fn)