import random
from threading import Lock

from Egg import Egg
from ExplorerAgent import ExplorerAgent
from Chicken import Chicken
from Observation import Observation


class Map:

    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height

        self.map = [["" for _ in range(width)] for _ in range(height)]

        self.chickens = []                                                      # Phase 3
        self.eggs = []
        self.nests = []
        self.stones = []

        self.lock = Lock()
        self.solved = False

    def addToMap(self, numEggs, numNests, numChickens):
        # TODO - corrigir isto, pq podem acontecer sobreposicoes de elementos com os randoms nao verificados

        for n in range(numEggs):
            # Random position
            x = random.randint(0, len(self.map[0]) - 1)
            y = random.randint(0, len(self.map) - 1)

            self.eggs.append(Egg(n, x, y))

        for _ in range(numNests):
            # Random position
            x = random.randint(0, len(self.map[0]) - 1)
            y = random.randint(0, len(self.map) - 1)

            self.nests.append((x, y))

        for n in range(numChickens):
            self.chickens.append(Chicken(n, 0, n))

    def observationFor(self, explorer: ExplorerAgent):                          # Phase 5.2
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

