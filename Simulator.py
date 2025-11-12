import concurrent.futures
import string
import time

from Agent import Agent
from Map import Map
from Sensor import Sensor


class Simulator:

    def __init__(self, mapWidth=5, mapHeight=5, numAgents=1, timeLimit=60):
        self.stop = False                                                           # Phase 1
        self.map = Map(mapWidth, mapHeight)                                         # Phase 2
        self.agents = [Agent().install(Sensor()) for n in range(numAgents)]         # Phase 3
        self.timeLimit = timeLimit

    def create(self, fileNameArgs):
        if not isinstance(fileNameArgs, string):
            raise TypeError("'fileNameArgs' should be of type string")
        pass #return Simulator

    def listAgents(self):
        return self.agents

    def execute(self):
        while not self.stop or self.timeLimit == 0:
            self.map.update()  # Phase 4 [cite: 56]

            # Phase 5
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(a.act) for a in self.agents]  # runs all agent "act()" methods in parallel

                concurrent.futures.wait(futures)                         # waits for all threads before continuing

            # TODO - verificar se ha conflitos com as açoes futuras (ex: 2 agentes ou mais a tentarem ir para o mesmo bloco)

            if self.map.solved:
                self.stop = True

            self.timeLimit -= 1
            time.sleep(0.5)

        self.saveResults()

    def saveResults(self):
        pass


if __name__ == "__main__":

    simulator = Simulator(5, 5, 1).create()

    print("Simulator created!")

    simulator.execute()

