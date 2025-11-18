from ExplorerAgent import ExplorerAgent
from Terrain import Terrain


class Sensor:

    def __init__(self, explorer: ExplorerAgent, terrain: Terrain, radius=3):
        self.explorer = explorer
        self.terrain = terrain
        self.radius = radius

    def getCurrentState(self):                       # Phase 5.1
        return self.terrain.observationFor(self.explorer)
