import random
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
                self.genotype[i] = Action.random_action()

    def __str__(self):
        return f"Explorer:{super().__str__()}. Inventory:{[item for item in self.inventory]}"