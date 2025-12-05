import time

from Simulators.Simulator import Simulator
from Worlds.CoopWorld import CoopWorld
from Worlds.ForagingWorld import ForagingWorld
from Worlds.World import World
from Simulators.Utilities import read_matrix_file_with_metadata


class SimulatorMotor(Simulator):

    def __init__(self, world: World, headless=True): # headless == True  ---->  no visualization
        self.time_limit = 100
        self.time_per_step = 0.05
        self.running = None
        self.world = world                                    # Phase 2 & 3
        self.headless = headless
        self.states = []

    @staticmethod
    def create(matrix_file):
        """
        Create a simulator from a matrix file.
        The matrix can be any size. Each character represents an object:
        . empty, E egg, N nest, S stone, W wall, F farol, C chicken
        """

        # Read the matrix
        try:
            matrix = read_matrix_file_with_metadata(matrix_file)
        except Exception as e:
            raise ValueError(f"Error reading matrix file: {e}")

        # Create world of matching size
        height = len(matrix)
        width = len(matrix[0])

        # Detect whether the matrix describes a coop world (has 'F') or foraging world
        has_farol = any('F' in row for row in matrix)

        if has_farol:
            print("Creating CoopWorld")
            # Step 2 — Create ID counters for coop world
            world = CoopWorld(width, height)
            world.initialize_map(matrix_file)  # TODO - pass matrix_file in .initialize_map()
            return SimulatorMotor(world)
        else:
            print("Creating ForagingWorld")
            world = ForagingWorld(width, height)
            # ForagingWorld has its own reader — delegate population to it and return early
            world.initialize_map(filename=matrix_file)
            return SimulatorMotor(world)


    def listAgents(self):
        if not self.running:
            print("Simulators not running. No agents to list.")
            return None

        return [a for a in self.world.agents]

    def execute(self):
        self.running = True                                                 # Phase 1

        while self.running:                                                 # -- loop --

            if not self.headless:
                self.world.show_world()

            for agent in self.world.agents:                                 # Phase 5
                agent.execute()


            self.saveState()

            # Check termination conditions
            if self.is_solved():                                             # Phase 9
                self.running = False

            # Manage time
            self.time_limit -= self.time_per_step

            if not self.headless:
                print(f"Time left: {round(self.time_limit, 1)} seconds")
                time.sleep(self.time_per_step * 2)

        self.shut_down()

    def is_solved(self):
        return self.world.solved or (self.time_limit <= 0)

    def shut_down(self):
        for agent in self.world.agents:
            print(f"Agent Reward: " + str(agent.reward))# Phase 10

        # TODO
        self.save_results("simulation_results.txt")                          # Phase 11

    def save_results(self, fileName="simulation_results.txt"):
        pass

    def save_state(self):
        # save the metrics: tempo e nr de passos, valores de novelty e fitness
        pass

if __name__ == "__main__":
    simulator = SimulatorMotor.create("farol_level1.txt")
    simulator.execute()
