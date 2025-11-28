import random

from Agent.Chicken import Chicken
from Items.Egg import Egg
from Agent.ExplorerAgent import ExplorerAgent
from Actions.Observation import Observation
from Items.Nest import Nest
from Items.Pickable import Pickable
from Items.Wall import Wall
from Environment import Environment


class World(Environment):

    def __init__(self, width=30, height=30):
        self.width = width
        self.height = height
        self.solved = False

        self.map = [[None for _ in range(width)] for _ in range(height)]
        self.agents = []                              # Phase 3
        self.eggs = []
        self.nests = []
        self.stones = []


    def observationFor(self, explorer: ExplorerAgent):  # Phase 5.2
        obs = Observation(explorer.id)
        sensor = explorer.sensor

        # TODO - usar Sensor?

        return explorer.observation(obs)

    def update(self):
        pass

    def act(self, action, agent: ExplorerAgent):  # Phase 7.1
        if action is None or agent is None:
            return False

        dx, dy = action
        ax, ay = agent

        newx = ax + dx
        newy = ay + dy

        # Within bounds
        if newx < 0 or newx >= len(self.map[0]) or newy < 0 or newy >= len(self.map):
            return False

        # Check for wall at destination
        if isinstance(self.map[newy][newx], Wall):
            return False

        agent.position = (newx, newy)
        obj_under_agent = self.map[newy][newx]
        reward = 0.0

        # Interaction with pickable objects
        if isinstance(obj_under_agent, Pickable):
            agent.storeItem(obj_under_agent)
        # Dropping items at nests (eggs/stones)
        elif isinstance(obj_under_agent, Nest):
            for item in agent.inventory:
                obj_under_agent.put(item)
                agent.discardItem(item)

        elif isinstance(obj_under_agent, Wall):
            pass #TODO

        return reward


    def initializeMap(self, numEggs, numNests, numChickens):
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
