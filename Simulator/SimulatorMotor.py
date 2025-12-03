import time

from Actions.Sensor import Sensor
from Agents.Chicken import Chicken
from Items.Wall import Wall
from Items.ChickenCoop import ChickenCoop
from Simulator.Simulator import Simulator
from Worlds.CoopWorld import CoopWorld
from Worlds.ForagingWorld import ForagingWorld
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
               
        #TODO : REMOVE MATRIX IMPLEMENTATION
        #TODO : IMPLEMENT FORAGING OR CHICKEN COOP

        # Step 1 — Read the matrix
        try:
            matrix = read_matrix_file_with_metadata(matrix_file)
        except Exception as e:
            raise ValueError(f"Error reading matrix file: {e}")

        # Step 3 — Create world of matching size
        height = len(matrix)
        width = len(matrix[0])

        # Detect whether the matrix describes a coop world (has 'F') or foraging world
        has_farol = any('F' in row for row in matrix)

        if has_farol:
            print("Creating CoopWorld")
            # Step 2 — Create ID counters for coop world
            world = CoopWorld(width, height)
            world.read_coop_file(matrix_file)
            # continue to parse the matrix below and populate world
            return SimulatorMotor(world)
        else:
            print("Creating ForagingWorld")
            world = ForagingWorld(width, height)
            # ForagingWorld has its own reader — delegate population to it and return early
            world.initialize_map(filename=matrix_file)
            return SimulatorMotor(world)

        # Step 4 — Return simulator with the world
        return SimulatorMotor(world)

    def listAgents(self):
        if not self.running:
            print("Simulator not running. No agents to list.")
            return None

        return [a for a in self.world.agents]

    def execute(self):
        self.running = True                                                 # Phase 1

        while self.running:                                                 # -- loop --

            self.world.show_world()

            for agent in self.world.agents:                                 # Phase 5
                agent.execute()

            self.saveState()

            # Check termination conditions
            if self.isSolved():                                             # Phase 9
                self.running = False

            # Manage time
            self.time_limit -= self.time_per_step


            # TODO - for debug:
            print(f"Time left: {round(self.time_limit, 1)} seconds")
            time.sleep(self.time_per_step * 2)                              # Slow down for visualization

        self.shutDownSimulation()
        for agent in self.world.agents:    
            print(f"Agent Reward: " + str(agent.reward))# Phase 10
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
    simulator.create("farol_level2.txt") # TODO : Placeholder file name

    simulator.execute()

    simulator.saveResults()