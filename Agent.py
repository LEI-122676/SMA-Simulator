import random
import time

from Action import Action
from Sensor import Sensor
from abc import ABC, abstractmethod


class Agent(ABC): #classe abstrata para os agentes

    def __init__(self, id, learner=False, steps=5000, genotype=None):
        super().__init__()
        self.id = id
        self.position = None
        self.sensor = None
        self.observed = set()

        self.steps = steps
        self.learner = learner
        self.genotype = genotype or [Action.random_action() for _ in range(self.steps)]
        self.combined_fitness = 0.0
        self.observed = set()

    @abstractmethod
    def create(self, fileNameArgs):
        """Optional factory method placeholder (not used in MVP)."""
        # TODO - something like this
        fileNameArgs = fileNameArgs.split(',')
        id = fileNameArgs[0]
        learner = fileNameArgs[1].lower() == 'true'

        return self.__init__(id, learner)

    @abstractmethod
    def observation(self, observation):
        self.observed.add(obs for obs in observation)

    @abstractmethod
    def act(self):
        """Execute a single step from the genotype. Returns the new position or None if finished."""
        if self.step_index >= len(self.genotype):
            return None

        dx, dy = self.genotype[self.step_index]
        x, y = self.position
        new_pos = (x + dx, y + dy)

        # update state
        self.position = new_pos
        self.path.append(new_pos)
        self.behavior.add(new_pos)
        self.step_index += 1

        return new_pos

    @abstractmethod
    def evaluateCurrentState(self, reward: float):
        # placeholder for reward handling
        pass

    @abstractmethod
    def install(self, sensor):
        self.sensor = sensor

    @abstractmethod
    def communicate(self, message, fromAgent):
        # placeholder for inter-agent comms
        pass

    @abstractmethod
    def __str__(self):
        return f"Agent:{self.id}"