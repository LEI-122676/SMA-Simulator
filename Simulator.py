import string
import time

from Agent import Agent
from Map import Map
from Sensor import Sensor


class Simulator:

    def __init__(self, mapWidth=5, mapHeight=5, numAgents=1, timeLimit=60):
        self.stop = False                                                           # Phase 1
        self.map = Map(mapWidth, mapHeight)                                         # Phase 2
        self.agents = [Agent(n) for n in range(numAgents)]                          # Phase 3
        self.timeLimit = timeLimit

    def create(self, fileNameArgs):
        if not isinstance(fileNameArgs, string):
            raise TypeError("'fileNameArgs' should be of type string")
        pass #return Simulator

    def listAgents(self):
        pass #return Agents

    def execute(self):
        pass

    def saveResults(self):
        pass


if __name__ == "__main__":

    simulator = Simulator(5, 5, 1)

    while not simulator.stop or simulator.timeLimit == 0:
        simulator.map.update()                                                      # Phase 4

        for a in simulator.agents:
            a.act()                                                                 # Phase 5


        simulator.map.act()

        if simulator.map.solved:
            simulator.stop = True
        
        simulator.timeLimit -= 1
        time.sleep(0.5)

    simulator.saveResults()