from Agent import Agent
from Map import Map


class Sensor:

    def __init__(self, id, mapWidth, mapHeight):
        self.agent = Agent(id)
        self.map = Map(mapWidth, mapHeight)

    def getCurrentState(self, agent):
        return self.map.observationFor(agent)
