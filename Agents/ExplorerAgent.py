import math

import numpy as np
from Actions.Action import Action
from Actions.Observation import Observation
from Actions.Sensor import Sensor
from Agents.Agent import Agent
from Items.Item import Item
from Items.Pickable import Pickable
from Simulators.Utilities import read_agent_config
from Items.Nest import Nest
from Items.ChickenCoop import ChickenCoop  # Import needed for heuristics


class ExplorerAgent(Agent):

    def __init__(self, learn_mode=True, steps=200, nn=None):
        self.position = None
        self.world = None

        self.learn_mode = learn_mode
        self.steps = steps

        # Neural Network (The Brain)
        self.nn = nn
        self.goal_vector = None  # Vector to goal (dx, dy) NOT NORMALIZED

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
        return cls(learn_mode, steps, nn=None)

    def observe(self, observation: Observation):
        self.observation = observation

    def act(self) -> Action:
        """
        Decides the next action.
        If in learn_mode (Neural Network), uses the brain.
        Otherwise, performs a heuristic fallback (Go to Coop / Random).
        """
        if self.learn_mode and self.nn is not None:
            return self.nn.decide_action(self)

        # --- Fallback / "Dumb" Logic ---
        return self._dumb_action()

    def _dumb_action(self):
        # 1. Try to go to Coop if visible/known
        if self.is_in_CoopWorld():
            # If we have a vector, use ChickenCoop static method logic (conceptually)
            if self.goal_vector:
                dx, dy = self.goal_vector
                if abs(dx) > abs(dy):
                    return Action.MOVE_EAST if dx > 0 else Action.MOVE_WEST
                else:
                    return Action.MOVE_NORTH if dy > 0 else Action.MOVE_SOUTH

        # 2. Foraging Logic (Simple Random Walk)
        return Action.random_action()

    def get_nn_inputs(self):
        """
        Constructs the input vector for the Neural Network.
        Size: 8 (Raycast) + 1 (Has Item) + 1 (Coop Distance) = 10 inputs
        """
        if self.observation is None:
            return [0.0] * 10

        inputs = []

        # 1. Raycast Inputs (8 directions)
        max_range = self.sensor.max_range
        directions = ["North", "NorthEast", "East", "SouthEast",
                      "South", "SouthWest", "West", "NorthWest"]

        for direction in directions:
            distance = self.observation.possible_actions.get(direction, 0)
            normalized_distance = distance / max_range if max_range > 0 else 0
            inputs.append(normalized_distance)

        # 2. Goal Input: Distance to Coop
        if self.is_in_CoopWorld():
            if self.goal_vector is not None:
                dx, dy = self.goal_vector
                max_x = self.world.width if self.world else 30
                max_y = self.world.height if self.world else 30
                norm_dx = dx / max_x
                norm_dy = dy / max_y
                inputs.extend([norm_dx, norm_dy])
            else:
                inputs.extend([0.0, 0.0])

        return inputs

    def evaluateCurrentState(self, reward: float):
        """ Accumulates "raw" reward during an Agent's life. """
        self.reward += reward

    def install(self, sensor: Sensor, world):
        self.sensor = sensor
        self.world = world
        self.update_goal_vector()

    def update_goal_vector(self):
        if self.sensor:
            self.goal_vector = self.sensor.get_goal_vector(self.position)

    def execute(self):
        # Gets observation
        observation = self.world.observation_for(self)
        self.observe(observation)

        # Decides what to do 
        action_to_take = self.act()

        # Tries to do it
        self.world.act(action_to_take, self)

        self.step_index += 1

        # Punish agent if he is stuck or oscillating based on movement history
        if len(self.path) > 0:
            if self.position == self.path[-1]:
                # Agent did not move (likely hit a wall)
                self.evaluateCurrentState(-4.0)

            elif len(self.path) > 1 and self.position == self.path[-2]:
                # Agent returned to the previous position (oscillating back and forth)
                self.evaluateCurrentState(-2.0)

        # Update state after move
        self.update_found_nest()
        self.behavior.add(self.position)
        self.path.append(self.position)

        # IMPORTANT: Update vector every step
        self.update_goal_vector()

    def storeItem(self, item: Pickable, x, y):
        self.sensor.world_map[y][x] = None
        item.pickUp()
        self.inventory.append(item)

    def discardItem(self, item: Pickable):
        item.drop()
        if item in self.inventory:
            self.inventory.remove(item)

    def is_in_CoopWorld(self):
        return self.goal_vector is not None

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