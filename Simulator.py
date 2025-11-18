import concurrent.futures
import threading
import time
from collections import defaultdict

from Agent import Agent
from Environment import Map


class Simulator:

    def __init__(self, timeLimit=60, timePerStep=0.5):
        self.running = None
        self.map = None
        self.timeLimit = timeLimit
        self.service_to_agents = defaultdict(set)
        self.lock = threading.Lock()
        self.timePerStep = timePerStep

    def create(self, fileNameArgs: str):
        numEggs = 10  # Default number of eggs
        numNests = 2  # Default number of nests
        numChickens = 1  # Default number of chickens

        self.map.initializeMap(numEggs, numNests, numChickens)

        pass #return Simulator

    def listAgents(self):
        if not self.running:
            print("Simulator not running. No agents to list.")
            return

        for a in self.map.chickens:
            print(a)

    def execute(self):
        self.running = True                                                             # Phase 1
        self.map = Map()                                                                # Phase 2 & 3

        while self.running:
            self.map.update()                                                      # Phase 4

            # Phase 5
            for chicken in self.map.chickens:
                chicken.execute()

            self.map.act(futures, self.agents)

            if self.map.solved or self.timeLimit == 0:
                self.running = False

            self.timeLimit -= self.timePerStep
            time.sleep(self.timePerStep)

        self.shutDownSimulation()
        self.saveResults("simulation_results.txt")

    def shutDownSimulation(self):
        pass

    def saveResults(self, fileName="simulation_results.txt"):
        pass

if __name__ == "__main__":

    simulator = Simulator()
    simulator.create("______") # TODO falta texto aq

    simulator.execute()

    simulator.saveResults()