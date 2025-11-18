from ExplorerAgent import ExplorerAgent
from Map import Map


class Sensor:

    def __init__(self, explorer: ExplorerAgent, map: Map):
        self.explorer = explorer
        self.map = map

    def getCurrentState(self):                       # Phase 5.1
        return self.map.observationFor(self.explorer)
