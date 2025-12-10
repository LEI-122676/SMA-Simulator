import math

import numpy as np
from Actions.Action import Action
from Actions.Observation import Observation
from Actions.Sensor import Sensor
from Agents.Agent import Agent
from Agents.NeuralNetwork import NeuralNetwork
from Items.ChickenCoop import ChickenCoop
from Items.Item import Item
from Items.Pickable import Pickable
from Simulators.Utilities import read_agent_config
from Items.Nest import Nest


class ExplorerAgent(Agent):

    def __init__(self, learn_mode=True, steps=200, nn=None):
        self.position = None
        self.world = None

        self.learn_mode = learn_mode
        self.steps = steps

        # Neural Network (The Brain)
        self.nn = nn
        self.coop_vector = None  # Vector to goal (dx, dy)

        self.sensor = None
        self.observation = None
        self.step_index = 0
        self.inventory: list[Pickable] = []
        self.communications = []
        self.found_nests = []

        self.behavior = set()
        self.path = []
        self.combined_fitness = 0.0
        self.reward = 0

        self.min_dist_reached = float('inf')

    @classmethod
    def create(cls, file_name: str):
        """
        Create an ExplorerAgent from a configuration file.
        """
        config = read_agent_config(file_name)

        learn_mode = config.get("learn_mode", "False").lower() == "true"
        steps = int(config.get("steps", 5000))

        # We initialize without a brain (nn=None).
        # The SimulatorMotor will inject the Neural Network later during the evolutionary process.
        return cls(learn_mode, steps, nn=None)

    def observe(self, observation: Observation):
        self.observation = observation

    def act(self) -> Action:
        """
        Decides the next action.
        If in learn_mode (Neural Network), uses the brain.
        Otherwise, performs a fallback or random action.
        """
        if self.learn_mode:
            # If we have a brain, use it
            if self.nn is not None:
                return self.nn_decide_action()
            # Fallback if no brain is installed
            else:
                return Action.random_action()
        else:
            # Legacy/Manual mode
            return Action.random_action()

    def get_nn_inputs(self):
        """
        Constructs the input vector for the Neural Network.
        Size: 8 (Raycast) + 1 (Has Item) + 1 (Coop Distance) = 10 inputs
        """
        if self.observation is None:
            return [0.0] * 9

        inputs = []

        # 1. Raycast Inputs (8 directions)
        # We normalize the distance so the NN gets values between 0.0 and 1.0
        max_range = self.sensor.max_range
        directions = ["North", "NorthEast", "East", "SouthEast",
                      "South", "SouthWest", "West", "NorthWest"]

        for direction in directions:
            distance = self.observation.possible_actions.get(direction, 0)

            # Normalize:
            # 0.0 = Obstacle is touching us (Very bad/Close)
            # 1.0 = Free space (Max range)
            normalized_distance = distance / max_range if max_range > 0 else 0
            inputs.append(normalized_distance)

        # 2. Goal Input: Distance to Coop
        if self.coop_vector is not None:
            dx, dy = self.coop_vector
            dist = math.sqrt(dx ** 2 + dy ** 2)
            # Use map diagonal as normalization factor
            max_diagonal = math.sqrt(self.world.width ** 2 + self.world.height ** 2) if self.world else 50
            norm_dist = 1.0 - (dist / max_diagonal)
            inputs.append(max(0.0, norm_dist))
        else:
            # If we don't know where the coop is, input 0
            inputs.append(0.0)

        return inputs

    def nn_decide_action(self):
        inputs = self.get_nn_inputs()  # Fetches the 10 inputs
        output_values = self.nn.forward(inputs)  # Now returns 4 floats

        # Pick the movement corresponding to the highest value
        best_action_index = np.argmax(output_values)
        possible_actions = [Action.MOVE_NORTH, Action.MOVE_SOUTH, Action.MOVE_EAST, Action.MOVE_WEST]

        return possible_actions[best_action_index]

    def evaluateCurrentState(self, reward: float):
        """ Accumulates "raw" reward during an Agent's life. """
        self.reward += reward

    def install(self, sensor: Sensor, world):
        self.sensor = sensor
        self.world = world
        # Initial update of vector so inputs are ready immediately
        self.update_coop_vector()

    def update_coop_vector(self):
        if self.sensor:
            # Updates the vector pointing to the shared goal (Coop or otherwise)
            self.coop_vector = self.sensor.get_coop_vector(self.position)

    def communicate(self, item: Item, from_agent: Agent):
        message = {
            'item_name': item.name,
            'item_id': item.id,
            'item_position': item.position,
            'sender': from_agent,
        }
        self.communications.append(message)

    def communicate_nest_positions(self, agents: list):
        return self.found_nests

    def broadcast_info(self, item: Item, agents: list):
        for agent in agents:
            if agent != self:
                agent.communicate(item, self)

    def execute(self):
        # Gets observation
        observation = self.world.observation_for(self)
        self.observe(observation)

        # Decides what to do (uses Neural Network if learn_mode=True)
        action_to_take = self.act()

        # Tries to do it
        self.world.act(action_to_take, self)

        self.step_index += 1

        # Update state after move
        self.update_found_nest()
        self.behavior.add(self.position)
        self.path.append(self.position)

        # IMPORTANT: Update vector every step so NN has fresh goal data
        self.update_coop_vector()

    def storeItem(self, item: Pickable, x, y):
        self.sensor.world_map[y][x] = None
        item.pickUp()
        self.inventory.append(item)

    def discardItem(self, item: Pickable):
        item.drop()
        if item in self.inventory:
            self.inventory.remove(item)

    def is_in_CoopWorld(self):
        return self.coop_vector is not None

    def update_found_nest(self):
        """
        Append new found nest positions to self.found_nests
        """
        x, y = self.position
        tile = self.world.map[y][x]
        if not isinstance(tile, Nest):
            return
        if tile.position not in self.found_nests:
            self.found_nests.append(tile.position)