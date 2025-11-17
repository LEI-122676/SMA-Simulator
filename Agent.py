import random
import threading
import time

from Action import Action
from Sensor import Sensor
from abc import ABC, abstractmethod


class Agent(threading.Thread, ABC):   # Threads
    #classe abstrata threaded para os agentes

    def __init__(self, id, learner=False, steps=5000, genotype=None):
        super().__init__()
        self.id = id
        self.learner = learner
        self.steps = steps
        self.genotype = genotype or [Action.random_action() for _ in range(self.steps)]

    def create(self, fileNameArgs):
        """Optional factory method placeholder (not used in MVP)."""
        # TODO - something like this
        fileNameArgs = fileNameArgs.split(',')
        id = fileNameArgs[0]
        learner = fileNameArgs[1].lower() == 'true'

        return self.__init__(id, learner)

    def observation(self, observation):
        # receive an Observation object (not used in MVP)
        return None

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

    def evaluateCurrentState(self, reward: float):
        # placeholder for reward handling
        pass

    def install(self, sensor):
        self.sensor = sensor
        return self

    def communicate(self, message, fromAgent):
        # placeholder for inter-agent comms
        pass

    def run(self):
        """Run the full genotype until completion or stop event."""
        # reset
        self.position = (0, 0)
        self.step_index = 0
        self.behavior = set()
        self.path = []

        self.behavior.add(self.position)
        self.path.append(self.position)

        for _ in range(len(self.genotype)):
            if self.stopEvent.is_set():
                break
            self.act()
            # small sleep to avoid burning CPU in threaded runs (keeps logs readable)
            time.sleep(0)

    # Convenience wrappers expected by Simulator
    def run_simulation(self):
        self.run()

    def calculate_objective_fitness(self):
        """Simple objective: coverage (number of unique visited cells)."""
        return len(self.behavior)

    def mutate(self, rate: float):
        """Randomly mutate genotype: with probability rate replace a gene with a random action."""
        for i in range(len(self.genotype)):
            if random.random() < rate:
                self.genotype[i] = random.choice(self.actions)

    def __str__(self):
        return f"Agent: {self.id}"