import concurrent.futures
import string
import threading
import time
from collections import defaultdict

from Agent import Agent
from Map import Map
from Sensor import Sensor


class Simulator:

    def __init__(self, mapWidth=5, mapHeight=5, numAgents=1, timeLimit=60):
        self.stop = False                                                           # Phase 1
        self.timeLimit = timeLimit

        self.map = Map(mapWidth, mapHeight)                                         # Phase 2
        self.agents = [Agent().install(Sensor()) for _ in range(numAgents)]         # Phase 3
        self.service_to_agents = defaultdict(set)
        self.lock = threading.Lock()


    def create(self, fileNameArgs: str):
        pass #return Simulator

    def listAgents(self):
        for a in self.agents:
            print(a)

    def execute(self):
        while not simulator.stop or simulator.timeLimit == 0:
            simulator.map.update()  # Phase 4

            # Phase 5
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(a.act) for a in
                           simulator.agents]      # runs all agent "act()" methods in parallel
                # TODO - cada alteracao a self.map é feita com "synchronized"
                concurrent.futures.wait(futures)  # waits for all threads before continuing

            simulator.map.act(futures, self.agents)

            if simulator.map.solved:
                simulator.stop = True

            simulator.timeLimit -= 1
            time.sleep(0.5)

    def saveResults(self):
        pass




if __name__ == "__main__":

    simulator = Simulator(100, 100, 1)
    simulator.create("______") # TODO falta texto aq

    simulator.execute()

    simulator.saveResults()