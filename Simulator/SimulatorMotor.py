import time
import random
import math

from Simulator.Simulator import Simulator
from Worlds.CoopWorld import CoopWorld
from Worlds.ForagingWorld import ForagingWorld
from Worlds.World import World
from Utilities import read_matrix_file_with_metadata

# --- EA Hyperparameters ---
POPULATION_SIZE = 50
NUM_GENERATIONS = 25
MUTATION_RATE = 0.05  # Increased slightly for better exploration
TOURNAMENT_SIZE = 3
N_ARCHIVE_ADD = 5  # Add top 5 most novel agents to archive
ELITISM_COUNT = 2  # Keep the best 2 agents unchanged


class SimulatorMotor(Simulator):

    def __init__(self, world: World, headless=False):
        self.time_limit = 100
        self.time_per_step = 0.05

        # HEADLESS MODE: If True, disables sleep() and prints for fast training
        self.headless = headless
        self.running = None
        self.world = world
        self.states = []

    @staticmethod
    def create(matrix_file, headless=False):
        """
        Factory method to create a simulation instance.
        """
        try:
            matrix = read_matrix_file_with_metadata(matrix_file)
        except Exception as e:
            raise ValueError(f"Error reading matrix file: {e}")

        height = len(matrix)
        width = len(matrix[0])
        has_farol = any('F' in row for row in matrix)

        if has_farol:
            if not headless: print("Creating CoopWorld")
            world = CoopWorld(width, height)
            world.initialize_map(matrix_file)
            return SimulatorMotor(world, headless)
        else:
            if not headless: print("Creating ForagingWorld")
            world = ForagingWorld(width, height)
            world.initialize_map(filename=matrix_file)
            return SimulatorMotor(world, headless)

    def listAgents(self):
        if not self.running:
            print("Simulator not running. No agents to list.")
        return self.world.agents

    def execute(self):
        """
        Runs one complete episode (simulation of life).
        Returns the agents after execution so we can extract their fitness.
        """
        self.running = True

        while self.running:
            # 1. Visualization (Skip in headless mode)
            if not self.headless:
                self.world.show_world()

            # 2. Agent Lifecycle
            for agent in self.world.agents:
                agent.execute()

            self.saveState()

            # 3. Termination Checks
            if self.isSolved():
                self.running = False

            self.time_limit -= self.time_per_step

            # 4. Time Management (Skip sleep in headless mode for speed)
            if not self.headless:
                print(f"Time left: {round(self.time_limit, 1)} seconds")
                time.sleep(self.time_per_step * 2)

                # Force stop if time runs out
            if self.time_limit <= 0:
                self.running = False

        self.shut_down()
        return self.world.agents  # Return agents to extract Fitness/Genotypes

    def isSolved(self):
        return self.world.solved

    def shut_down(self):
        pass

    def save_results(self, fileName="simulation_results.txt"):
        pass

    def save_state(self):
        pass
