import string
import time

from Agent import Agent
from World import World


class Simulator:

    def __init__(self, worldSize, numAgents):
        self.world = World(worldSize)
        self.agents = [Agent(n) for n in numAgents]

    def create(self, fileNameArgs):
        if not isinstance(fileNameArgs, string):
            raise TypeError("'fileNameArgs' should be of type string")
        pass #return Simulator

    def listAgents(self):
        pass #return Agents

    def execute(self):
        pass

if __name__ == "__main__":

    map = World()

    while not map.stop:
        map.update()

        x, y = map.get_action()
        obj = map.get_object_here(x, y)

        map.agentx = x
        map.agenty = y

        time.sleep(0.5)

