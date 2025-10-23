import string
import time

from Agent import Agent
from Map import Map
from Sensor import Sensor


class Simulator:

    def __init__(self, worldWidth, worldHeight, numAgents, timeLimit):
        self.stop = False                                                   # Phase 1
        self.map = Map(worldWidth, worldHeight)                             # Phase 2
        self.agents = [Agent(n).install(Sensor()) for n in numAgents]       # Phase 3
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

    while not simulator.stop:
        simulator.map.update()                                              # Phase 4

        for a in simulator.agents:
            a.act()                                                         # Phase 5


        simulator.map.act()

        if simulator.map.solved or simulator.timeLimit == 0:
            break
        
        simulator.timeLimit -= 1
        time.sleep(0.5)

    simulator.saveResults()