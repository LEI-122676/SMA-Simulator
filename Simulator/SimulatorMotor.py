import time

from Agents.Chicken import Chicken
from Items.ChickenCoop import ChickenCoop
from Items.Wall import Wall
from Simulator.Simulator import Simulator
from Worlds.CoopWorld import CoopWorld
from Worlds.World import World
from Utilities import read_matrix_file_with_metadata

class SimulatorMotor(Simulator):

    def __init__(self, world: World, time_limit=500, time_per_step=0.1):
        self.time_limit = time_limit
        self.time_per_step = time_per_step

        self.running = None
        self.world = world                                    # Phase 2 & 3

        self.states = []

    @staticmethod
    def create(matrix_file):
        """
        Create a simulator from a matrix file.
        The matrix can be any size. Each character represents an object:
        . empty, E egg, N nest, S stone, W wall, F farol, C chicken
        """

        # Step 1 — Read the matrix
        try:
            matrix = read_matrix_file_with_metadata(matrix_file)
        except Exception as e:
            raise ValueError(f"Error reading matrix file: {e}")

        # Step 2 — Create ID counters
        id_counter = {"egg": 0, "chicken": 0, "nest": 0, "stone": 0, "wall": 0, "farol": 0}
        
        # Step 3 — Create world of matching size
        height = len(matrix)
        width = len(matrix[0])
        world = CoopWorld(width, height)

        for y in range(height):
            for x in range(width):
                char = matrix[y][x]

                if char == ".":
                    continue
                    """
                elif char == "E":
                    egg = Egg(id_counter["egg"], x, y)
                    world.eggs.append(egg)
                    world.map[y][x] = egg
                    id_counter["egg"] += 1
                elif char == "N":
                    world.nests.append((x, y))
                    world.map[y][x] = Nest(id_counter["nest"], x, y)
                    id_counter["nest"] += 1
                elif char == "S":
                    world.stones.append((x, y))
                    world.map[y][x] = Stone(id_counter["stone"], x, y)
                    id_counter["stone"] += 1
                    """
                elif char == "W":
                    wall = Wall(id_counter["wall"], x, y)
                    world.map[y][x] = wall
                    id_counter["wall"] += 1
                elif char == "C":
                    chicken = Chicken(id_counter["chicken"], x, y)
                    world.agents.append(chicken)
                    world.map[y][x] = chicken
                    id_counter["chicken"] += 1
                elif char == "F":
                    world.map[y][x] = ChickenCoop(id_counter["farol"], x, y)
                    id_counter["farol"] += 1
                else:
                    raise ValueError(f"Unknown character '{char}' at ({x},{y})")

        # Step 4 — Return simulator with the world
        return SimulatorMotor(world)


    def listAgents(self):
        if not self.running:
            print("Simulator not running. No agents to list.")
            return None

        return [a for a in self.world.chickens]

    def execute(self):
        self.running = True                                                 # Phase 1

        while self.running:                                                 # -- loop --
            self.world.update()                                             # Phase 4

            for agent in self.world.agents:                                 # Phase 5
                agent.execute()

            self.saveState()

            # Check termination conditions
            if self.isSolved():                                             # Phase 9
                self.running = False

            # Manage time
            self.time_limit -= self.time_per_step
            time.sleep(self.time_per_step)

        self.shutDownSimulation()                                           # Phase 10
        self.saveResults("simulation_results.txt")                          # Phase 11

    def isSolved(self):
        return self.world.solved or (self.time_limit <= 0)

    def shutDownSimulation(self):
        pass

    def saveResults(self, fileName="simulation_results.txt"):
        pass

    def saveState(self):
        # save the metrics: tempo e nr de passos, valores de novelty e fitness
        pass

if __name__ == "__main__":

    simulator = SimulatorMotor()
    simulator.create("example_file_farol.txt") # TODO : Placeholder file name

    simulator.execute()

    simulator.saveResults()