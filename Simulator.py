import concurrent.futures
import threading
import time
from collections import defaultdict

from Agent import Agent
from Map import Map


class Simulator:

    def __init__(self, timeLimit=60):
        self.running = None
        self.map = None
        self.timeLimit = timeLimit
        self.service_to_agents = defaultdict(set)
        self.lock = threading.Lock()

    def create(self, fileNameArgs: str):
        numEggs = 10  # Default number of eggs
        numNests = 2  # Default number of nests
        numChickens = 1  # Default number of chickens

        self.map.addToMap(numEggs, numNests, numChickens)

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

        while simulator.running or simulator.timeLimit == 0:
            simulator.map.update()                                                      # Phase 4

            # Phase 5
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(c.act) for c in self.map.chickens]      # runs all agent "act()" methods in parallel

                # TODO - cada alteracao a self.map é feita com "synchronized"

                concurrent.futures.wait(futures)  # waits for all threads before continuing

            self.map.act(futures, self.agents)

            if self.map.solved:
                self.running = False

            self.timeLimit -= 1
            time.sleep(0.5)

        self.saveResults("simulation_results.txt")

    def saveResults(self, fileName="simulation_results.txt"):
        pass


if __name__ == "__main__":

    simulator = Simulator()
    simulator.create("______") # TODO falta texto aq

    simulator.execute()

    simulator.saveResults()