import random

from Items.Egg import Egg
from Items.Nest import Nest
from Items.Stone import Stone
from Items.Wall import Wall
from Worlds.World import World
from Agents.Chicken import Chicken
from Actions.Sensor import Sensor

class ForagingWorld(World):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.stones = []
        self.nests = []
        self.eggs = []

    def initialize_map(self, numEggs=1, numNests=1, filename=None):
        
        if filename is None:
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
                egg = Egg(n)
                egg.position = (x, y)
                self.eggs.append(egg)
                self.map[y][x] = egg

            # Colocar os ninhos -> calcular primeiro a sua capacidade
            capacity = (numEggs // numNests) + (1 if numEggs % numNests > 0 else 0)

            for n in range(numNests):
                x, y = place_unique()
                nest = Nest(n)
                # set_capacity is the defined method on Nest
                nest.set_capacity(capacity)
                nest.position = (x, y)
                self.nests.append(nest)
                self.map[y][x] = nest

        else:
            self.read_foraging_file(filename)

    def is_solved(self):
        # cada ovo tem que estar not picked_up e tem de estar num ninho da lista de ninhos para o mundo ser resolvido
        return all((not egg.picked_up) and any(nest.position == egg.position for nest in self.nests) for egg in self.eggs)

    def read_foraging_file(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

        id_counters = {"egg": 0, "nest": 0, "stone": 0, "wall": 0, "chicken": 0}

        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip()):
                if char == ".":
                    continue
                elif char == "E":
                    egg = Egg(id_counters["egg"])
                    egg.position = (x, y)
                    self.eggs.append(egg)
                    self.map[y][x] = egg
                    id_counters["egg"] += 1
                elif char == "N":
                    nest = Nest(id_counters["nest"])
                    nest.position = (x, y)
                    self.nests.append(nest)
                    self.map[y][x] = nest
                    id_counters["nest"] += 1
                elif char == "S":
                    stone = Stone(id_counters["stone"])
                    stone.position = (x, y)
                    self.stones.append(stone)
                    self.map[y][x] = stone
                    id_counters["stone"] += 1
                elif char == "W":
                    wall = Wall(id_counters["wall"])
                    wall.position = (x, y)
                    self.map[y][x] = wall
                    id_counters["wall"] += 1
                elif char == "C":
                    chicken = Chicken()
                    self.add_agent(chicken,(x, y))
                    id_counters["chicken"] += 1
                else:
                    raise ValueError(f"Unknown character '{char}' at ({x},{y})")