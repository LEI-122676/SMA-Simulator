import random

from Agents.Chicken import Chicken
from Agents.ExplorerAgent import ExplorerAgent
from Items.ChickenCoop import ChickenCoop
from Items.Wall import Wall
from Worlds.World import World


class CoopWorld(World):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.chicken_coop = None

    def initialize_map(self, filename=None):

        # Resets everything
        self.map = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.agents = []
        self.chicken_coop = None

        if filename is None:
            attempts = 0
            max_attempts = self.width * self.height

            while attempts < max_attempts:
                x = random.randrange(self.width)
                y = random.randrange(self.height)
                obj = self.map[y][x]

                isOccupied = any(agent.position == (x,y) for agent in self.agents)

                if isinstance(obj, Wall) or isOccupied:
                    attempts += 1
                    continue

                self.chicken_coop = ChickenCoop(x,y)
                self.map[y][x] = self.chicken_coop
                break
        else:
            self.read_coop_file(filename)

        """
        # Colocar as galinhas -> todas lado a lado na primeira fila
        for n in range(numChickens):
            x, y = n, 0
            chicken = Chicken(n, x, y)
            self.agents.append(chicken)
            self.map[y][x] = chicken
        """

    def read_coop_file(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

        id_counter = {"chicken": 0, "wall": 0, "farol": 0}

        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip()):
                if char == ".":
                    continue
                elif char == "W":
                    wall = Wall((id_counter["wall"]+1) * 100 )
                    self.map[y][x] = wall
                    id_counter["wall"] += 1
                elif char == "F":
                    coop = ChickenCoop(x, y)
                    self.map[y][x] = coop
                    self.chicken_coop = coop
                    id_counter["farol"] += 1
                elif char == "C":
                    chicken = Chicken()
                    self.add_agent(chicken,(x, y))
                    id_counter["chicken"] += 1
                else:
                    raise ValueError(f"Unknown character '{char}' at ({x},{y})")


    def is_solved(self):
        for explorer in self.agents:
            if isinstance(explorer, ExplorerAgent) and explorer.position != self.chicken_coop.pos:
                return False

        return True
