import random
import threading

from Agent import Agent
from Sensor import Sensor


class ExplorerAgent(Agent):

    def __init__(self, id, learningMode=True, genotype=None):
        super().__init__(id)
        self.isLearningAgent = True
        self.learningMode = learningMode

        self.inventory = []
        self.sensor = Sensor()
        self.genotype = genotype

        self.actions = [(0, 1), (0, -1), (-1, 0), (1, 0)]  # N, S, W, E
        self.steps = 5000

        # genotype -> the sequence of actions the agent will take.
        self.genotype = self.genotype or [random.choice(self.actions) for _ in range(self.steps)]

        self.behavior = set()  # store unique coordinates visited by the agent during a simulation, used to measure exploration
        self.path = []  # store the sequence of coordinates visited by the agent during a simulation, preserving the order

        self.noveltyScore = 0.0
        self.combinedFitness = 0.0

        self.stopEvent = threading.Event()  # control flag

        # runtime state
        self.position = (0, 0)
        self.step_index = 0

    def pickUp(self, item):
        self.inventory.append(item)
        print(f"ExplorerAgent {self.id} picked up {item.name}")

    def __str__(self):
        return f"Explorer{super().__str__()} Inventory: {[item.name for item in self.inventory]}"