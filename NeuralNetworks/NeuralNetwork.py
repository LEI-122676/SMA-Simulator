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
        try:
            w = np.array(weights)
            self.hidden_weights = []
            self.hidden_biases = []
            start_w = 0
            input_size = self.input_size

            for n in self.hidden_architecture:
                end_w = start_w + (input_size * n)
                # Check for array bounds
                if end_w > len(w):
                    raise ValueError(
                        f"Weight mismatch: Expected more weights for hidden layer (needed {end_w}, got {len(w)})")

                self.hidden_weights.append(w[start_w:end_w].reshape(input_size, n))
                start_w = end_w

                # Biases
                if start_w + n > len(w):
                    raise ValueError("Weight mismatch: Not enough weights for biases")

                self.hidden_biases.append(w[start_w:start_w + n])
                start_w += n
                input_size = n

            # Final Layer
            end_w = start_w + (input_size * 4)
            if end_w > len(w):
                raise ValueError("Weight mismatch: Not enough weights for output layer")

            self.output_weights = w[start_w:end_w].reshape(input_size, 4)
            self.output_bias = w[end_w:]

        except (ValueError, IndexError) as e:
            print(f"[Error] Failed to load weights: {e}")
            print("The saved genome likely belongs to a different Neural Network architecture (e.g. Coop vs Foraging).")
            # Re-initialize random weights to prevent crash, though agent will be dumb
            print("Re-initializing random weights for this agent.")
            # Simple random init logic as fallback is complex here without structure knowledge,
            # effectively the agent will crash on forward() if weights aren't set.
            # So we set them to zeros or randoms matching current structure:
            self._init_random_weights()

    def _init_random_weights(self):
        """ Helper to set random weights if loading fails """
        input_size = self.input_size
        self.hidden_weights = []
        self.hidden_biases = []

        for n in self.hidden_architecture:
            self.hidden_weights.append(np.random.randn(input_size, n) * 0.1)
            self.hidden_biases.append(np.zeros(n))
            input_size = n

        self.output_weights = np.random.randn(input_size, 4) * 0.1
        self.output_bias = np.zeros(4)

    def forward(self, x):
        if not self.hidden_weights:
            return np.zeros(4)  # Safety for uninitialized net

        a = np.array(x)
        for i in range(len(self.hidden_architecture)):
            z = np.dot(a, self.hidden_weights[i]) + self.hidden_biases[i]
            a = self.hidden_activation(z)
        output = np.dot(a, self.output_weights) + self.output_bias
        return self.output_activation(output) if self.output_activation else output