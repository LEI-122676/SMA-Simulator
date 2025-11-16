from Chicken import Chicken
from Map import Map


class Sensor:

    def __init__(self, chicken: Chicken, map: Map):
        self.chicken = chicken
        self.map = map

    def getCurrentState(self):                       # Phase 5.1
        return self.map.observationFor(self.chicken)
