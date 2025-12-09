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
        # Resets everything (for next simulation run)
        self.reset()
        self.chicken_coop = None

        if filename:
            self.read_coop_file(filename)
        else:
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

    def read_coop_file(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

        id_counter = {"chicken": 0, "wall": 0, "farol": 0}

        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip()):
                if char == ".":
                    continue
                elif char == "W":
                    wall = Wall((id_counter["wall"]+1) * 100, x, y)
                    self.map[y][x] = wall
                    id_counter["wall"] += 1
                elif char == "F":
                    coop = ChickenCoop(x, y)
                    self.map[y][x] = coop
                    self.chicken_coop = coop
                    id_counter["farol"] += 1
                elif char == "C":
                    chicken = Chicken.create("Agents/chicken_compose.txt")
                    self.add_agent(chicken,(x, y))
                    id_counter["chicken"] += 1
                else:
                    raise ValueError(f"Unknown character '{char}' at ({x},{y})")


    def is_over(self):
        # Checks if all agents are out of steps
        if all(agent.step_index >= agent.steps for agent in self.agents):
            return True

        for explorer in self.agents:
            if isinstance(explorer, ExplorerAgent) and explorer.position != self.chicken_coop.position:
                return False

        return True