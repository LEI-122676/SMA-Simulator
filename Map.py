from threading import Lock

from ExplorerAgent import ExplorerAgent
from Chicken import Chicken
from Observation import Observation
from Sensor import Sensor





class Map:

    def __init__(self, width, height):
        self.map = [["" for _ in range(width)] for _ in range(height)]
        self.sensors = self.setUpSensors()
        self.items = self.createItems()
        
        self.lock = Lock()
        self.solved = False
      

    def observationFor(self, explorer: ExplorerAgent):                        # Phase 5.2
        obs = Observation()
        
        # TODO - usar Sensor?
        
        return explorer.observation(obs)

    def update(self):
        pass

    def act(self, action, agent):
        with self.lock:
            # Calculates future position
            future = (agent.x + action[0], agent.y + action[1])

            # Check if future position is within map bounds
            if self.isActionValid(future):
                agent.act(action)

    def isActionValid(self, future):
        x, y = future
        if x < 0 or x >= len(self.map[0]) or y < 0 or y >= len(self.map):
            return False

        if self.map[y][x] != " ":           # F = Fence
            return False

        return True

    def setUpSensors(self):
        pass

    def createItems(self):
        pass