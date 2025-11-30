import random

from Items.Egg import Egg
from Items.Nest import Nest
from Items.Stone import Stone
from Worlds.World import World


class ForagingWorld(World):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.stones = []
        self.nests = []
        self.eggs = []

    def initializeMap(self, numEggs=1, numNests=1):
        # Certificar que a posição está livre
        def place_unique():
            while True:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if self.map[y][x] is None:
                    return x, y

        # Colocar os ovos
        for n in range(numEggs):
            x, y = place_unique()
            egg = Egg(n, x, y)
            self.eggs.append(egg)
            self.map[y][x] = egg

        # Colocar os ninhos -> calcular primeiro a sua capacidade
        capacity = (numEggs // numNests) + (1 if numEggs % numNests > 0 else 0)

        for n in range(numNests):
            x, y = place_unique()
            nest = Nest(n, x, y).setCapacity(capacity)
            self.nests.append(nest)
            self.map[y][x] = nest

        """
        # Colocar as galinhas -> todas lado a lado na primeira fila
        for n in range(numChickens):
            x, y = n, 0
            chicken = Chicken(n, x, y)
            self.agents.append(chicken)
            self.map[y][x] = chicken
        """

    def is_solved(self):
        # cada ovo tem que estar not picked_up e tem de estar num ninho da lista de ninhos para o mundo ser resolvido
        return all((not egg.picked_up) and any(nest.position == egg.position for nest in self.nests) for egg in self.eggs)

    def showWorld(self):
    # Show the world map, agents, eggs, stones, and nests
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                obj = self.map[y][x]
                if obj is None:
                    row += ". "
                elif any(agent.position == (x, y) for agent in self.agents):
                    row += "C "
                elif any(egg.position == (x, y) for egg in self.eggs):
                    row += "E "
                elif any(nest.position == (x, y) for nest in self.nests):
                    row += "N "
                elif any(stone.position == (x, y) for stone in self.stones):
                    row += "S "
                else:
                    row += "W "
            print(row)
