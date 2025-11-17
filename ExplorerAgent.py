import threading

from Action import Action
from Agent import Agent


class ExplorerAgent(Agent):

    def __init__(self, id, x, y, learnMode, steps, genotype):
        super().__init__(id, learnMode, genotype, steps)

        self.inventory = []
        self.sensor = None

        self.behavior = set()   # store unique coordinates visited by the agent during a simulation, used to measure exploration
        self.path = []          # store the sequence of coordinates visited by the agent during a simulation, preserving the order

        self.steps = steps
        self.noveltyScore = 0.0
        self.combinedFitness = 0.0

        self.stopEvent = threading.Event()  # control flag

        # runtime state
        self.x = x
        self.y = y
        self.step_index = 0

    def pickUp(self, item):
        self.inventory.append(item)
        print(f"ExplorerAgent:{self.id} picked up {item}")

    def __str__(self):
        return f"Explorer{super().__str__()} Inventory: {[item.name for item in self.inventory]}"