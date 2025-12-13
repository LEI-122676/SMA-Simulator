import random

from Items.Egg import Egg
from Items.Nest import Nest
from Items.Stone import Stone
from Items.Wall import Wall
from Worlds.World import World
from Agents.Chicken import Chicken


class ForagingWorld(World):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.stones = []
        self.nests = []
        self.eggs = []

    def initialize_map(self, file_name=None, numEggs=1, numNests=1):
        # Resets everything (for next simulation run)
        self.reset()
        self.eggs = []
        self.nests = []
        self.stones = []

        if file_name:
            self.read_foraging_file(file_name)
        else:
            # Helper to find empty spot
            def place_unique():
                while True:
                    x = random.randint(0, self.width - 1)
                    y = random.randint(0, self.height - 1)
                    if self.map[y][x] is None:
                        return x, y

            # Place Eggs
            for n in range(numEggs):
                x, y = place_unique()
                # Pass x, y to constructor
                egg = Egg(n, x, y)
                self.eggs.append(egg)
                self.map[y][x] = egg

            # Place Nests
            capacity = (numEggs // numNests) + (1 if numEggs % numNests > 0 else 0)

            for n in range(numNests):
                x, y = place_unique()
                nest = Nest(n, x, y)
                nest.set_capacity(capacity)
                self.nests.append(nest)
                self.map[y][x] = nest

    def read_foraging_file(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

        id_counters = {"egg": 0, "nest": 0, "stone": 0, "wall": 0, "chicken": 0}

        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip()):
                if char == ".":
                    continue
                elif char == "E":
                    egg = Egg(id_counters["egg"], x, y)
                    self.eggs.append(egg)
                    self.map[y][x] = egg
                    id_counters["egg"] += 1
                elif char == "N":
                    nest = Nest(id_counters["nest"], x, y)
                    self.nests.append(nest)
                    self.map[y][x] = nest
                    id_counters["nest"] += 1
                elif char == "S":
                    stone = Stone(id_counters["stone"], x, y)
                    self.stones.append(stone)
                    self.map[y][x] = stone
                    id_counters["stone"] += 1
                elif char == "W":
                    wall = Wall(id_counters["wall"], x, y)
                    self.map[y][x] = wall
                    id_counters["wall"] += 1
                elif char == "C":
                    # Create Chicken Agent
                    chicken = Chicken.create("Agents/chicken_compose.txt")
                    self.add_agent(chicken, (x, y))
                    id_counters["chicken"] += 1
                else:
                    raise ValueError(f"Unknown character '{char}' at ({x},{y})")

        # Set capacities for nests after counting eggs
        if self.nests:
            capacity = (len(self.eggs) // len(self.nests)) + (1 if len(self.eggs) % len(self.nests) > 0 else 0)
            for nest in self.nests:
                nest.set_capacity(capacity)

    def is_solved(self):
        # World is solved if all eggs are in nests
        if not self.eggs:
            return False

        if all((not egg.picked_up) and any(nest.position == egg.position for nest in self.nests) for egg in self.eggs):
            return True
        return False

    def is_over(self):
        # 1. All agents out of steps
        if all(agent.step_index >= agent.steps for agent in self.agents):
            return True
        # 2. Solved
        if self.is_solved():
            return True
        return False