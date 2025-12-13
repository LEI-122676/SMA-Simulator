import numpy as np
from abc import ABC, abstractmethod
from Actions.Action import Action

class NeuralNetwork(ABC):

    def __init__(self, input_size, hidden_architecture, hidden_activation, output_activation):
        self.input_size = input_size
        self.hidden_architecture = hidden_architecture
        self.hidden_activation = hidden_activation
        self.output_activation = output_activation

        self.hidden_weights = []
        self.hidden_biases = []
        self.output_weights = None
        self.output_bias = None

    @classmethod
    @abstractmethod
    def get_input_size(cls):
        pass

    @abstractmethod
    def get_inputs(self, agent) -> list:
        """ Extracts the specific inputs this network needs from the agent. """
        pass

    def decide_action(self, agent):
        """
        The Brain Logic:
        1. Get inputs from agent
        2. Forward pass
        3. Interpret output as Action
        """
        inputs = self.get_inputs(agent)
        output_values = self.forward(inputs)

        best_action_index = np.argmax(output_values)
        possible_actions = [Action.MOVE_NORTH, Action.MOVE_SOUTH, Action.MOVE_EAST, Action.MOVE_WEST]

        if best_action_index < len(possible_actions):
            return possible_actions[best_action_index]
        return Action.random_action()

    def compute_num_weights(self):
        total = 0
        input_size = self.input_size

        for n in self.hidden_architecture:
            total += (input_size + 1) * n
            input_size = n

        total += (input_size + 1) * 4  # 4 neurons for Output
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

        end_w = start_w + (input_size * 4)
        self.output_weights = w[start_w:end_w].reshape(input_size, 4)
        self.output_bias = w[end_w:]

    def forward(self, x):
        a = np.array(x)
        for i in range(len(self.hidden_architecture)):
            z = np.dot(a, self.hidden_weights[i]) + self.hidden_biases[i]
            a = self.hidden_activation(z)
        output = np.dot(a, self.output_weights) + self.output_bias
        return self.output_activation(output) if self.output_activation else output