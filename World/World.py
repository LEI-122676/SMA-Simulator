import random

from Actions.Action import Action
from Agent.Chicken import Chicken
from Items.Egg import Egg
from World.Environment import Environment
from Agent.ExplorerAgent import ExplorerAgent
from Items.Item import Item
from Actions.Observation import Observation
from Obstacle import Obstacle


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

    def act(self, action, agent):
        future_pos = self.is_valid_action(action, agent.position)  # TODO - acho q n é preciso checkar a validade aq pq vai sempre receber uma acao valida right?
        if not future_pos:
            return
        agent.position = future_pos

        # TODO - interagir com o objeto na posicao futura
        fx, fy = future_pos
        obj = self.map[fy][fx]
        if (isinstance(obj, Item)):
            pass

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

    # Phase 7.1
    def is_valid_action(self, action_to_validate: Action, explorer_pos):
        """
        Validate if the action is possible for the explorer in the current world state.
        Returns the new position (x, y) if valid, otherwise returns False.
        """

        if action_to_validate is None:
            return False

        dx, dy = action_to_validate
        px, py = explorer_pos

        x = px + dx
        y = py + dy

        # Within bounds
        if x < 0 or x >= len(self.map[0]) or y < 0 or y >= len(self.map):
            return False

        # Check for wall at destination
        if isinstance(self.map[y][x], Obstacle):
            return False

        return x, y
