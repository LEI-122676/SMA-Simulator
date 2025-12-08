import numpy as np

from Actions.Action import Action


class NeuralNetwork:

    def __init__(self, input_size, output_size, hidden_architecture, hidden_activation, output_activation):
        self.input_size = input_size #dado pelo sensor?
        self.output_size = output_size

        self.hidden_architecture = hidden_architecture #tuple with the number of neurons in each hidden layer: (5, 2)-> 2 hidden layers, 1st has 5n and 2nd has 2n
        # The activations are functions
        self.hidden_activation = hidden_activation
        self.output_activation = output_activation

    def compute_num_weights(self):
        total = 0
        input_size = self.input_size
        output_size = len(Action)

        for n in self.hidden_architecture:
            total += n  # Biases
            total += input_size * n
            input_size = n

        total += output_size  # Bias do output
        total += input_size * output_size  # Pesos do output

        return total

    def load_weights(self, weights):
        w = np.array(weights)

        self.hidden_weights = []
        self.hidden_biases = []

        start_w = 0
        input_size = self.input_size
        for n in self.hidden_architecture:
            end_w = start_w + (input_size + 1) * n
            self.hidden_biases.append(w[start_w:start_w + n])
            self.hidden_weights.append(w[start_w + n:end_w].reshape(input_size, n))
            start_w = end_w
            input_size = n

        self.output_bias = w[start_w:start_w + self.output_size]
        self.output_weights = w[start_w + self.output_size:].reshape(input_size, self.output_size)

    def forward(self, x):
        a = np.array(x)
        for i in range(len(self.hidden_architecture)):
            z = np.dot(a, self.hidden_weights[i]) + self.hidden_biases[i]
            a = self.hidden_activation(z)
        output = np.dot(a, self.output_weights) + self.output_bias
        return self.output_activation(output)


def create_network_architecture(input_size):
    # hidden_architecture = ()                      # () = 1 perceptrão (input -> output)
    # hidden_architecture = (3,)                      # (x,) = 1 camada escondida com x neurónios
    hidden_architecture = (8,)

    hidden_fn = lambda x: 1 / (1 + np.exp(-x))  # Função logística
    output_fn = lambda x: x

    output_size = 4 # N, S, E, W
    return NeuralNetwork(input_size, output_size, hidden_architecture, hidden_fn, output_fn)