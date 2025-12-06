import time
import random
import GeneticUtils as GU
from Actions.Action import Action

# --- Imports for World/Agent Management ---
from Worlds.CoopWorld import CoopWorld
from Worlds.ForagingWorld import ForagingWorld
from Simulators.Simulator import Simulator
from Utilities import read_matrix_file_with_metadata


class SimulatorMotor(Simulator):
    # --- EA Hyperparameters (Config) ---
    POPULATION_SIZE = 50
    NUM_GENERATIONS = 30
    MUTATION_RATE = 0.02
    TOURNAMENT_SIZE = 4
    N_ARCHIVE_ADD = 3
    ELITISM_COUNT = 2

    # Simulation Settings
    STEPS = 500  # Genome length (Number of actions per agent)
    TIME_LIMIT = 200
    TIME_PER_STEP_HEADLESS = 0.0
    TIME_PER_STEP_VISUAL = 0.05

    def __init__(self, world, map_file_path, headless=False):
        """
        Initialize with a 'template' world, the file path to recreate it,
        and a headless configuration.
        """
        self.world = world
        self.map_file_path = map_file_path
        self.running = False

        # Configuration for the simulation run
        self.config_headless = headless

        # Dynamic state variable (toggled during execution)
        self.headless = headless

    @staticmethod
    def create(matrix_file, headless=False):
        """
        Factory method: Reads the file and returns a configured SimulatorMotor.
        Accepts a headless boolean to control visualization.
        """
        try:
            matrix = read_matrix_file_with_metadata(matrix_file)
        except Exception as e:
            raise ValueError(f"Error reading matrix file: {e}")

        height = len(matrix)
        width = len(matrix[0])
        has_farol = any('F' in row for row in matrix)

        if has_farol:
            print(f"--- Initializing CoopWorld ({width}x{height}) ---")
            world = CoopWorld(width, height)
            world.initialize_map(matrix_file)
        else:
            print(f"--- Initializing ForagingWorld ({width}x{height}) ---")
            world = ForagingWorld(width, height)
            world.initialize_map(filename=matrix_file)

        return SimulatorMotor(world, matrix_file, headless)

    def listAgents(self):
        if not self.running:
            print("Simulators not running. No agents to list.")
            return None

        return [a for a in self.world.agents]

    def execute(self):
        """
        The 'Black Box' method.
        Runs the full Evolutionary Algorithm process.
        """
        print(f"--- Starting Evolutionary Process ---")
        print(f"Generations: {self.NUM_GENERATIONS} | Population: {self.POPULATION_SIZE}")

        # 1. Setup Evolution
        archive = []
        action_space = Action.get_all_actions()

        # 2. Initialize Population (Genotypes)
        # Uses the constant STEPS instead of checking agent instances
        population = []
        for _ in range(self.POPULATION_SIZE):
            genes = [Action.random_action() for _ in range(self.STEPS)]
            population.append(genes)

        best_result_global = None

        # 3. Main Generational Loop
        for gen in range(self.NUM_GENERATIONS):

            evaluated_results = []  # Stores {stats, genotype}

            # --- A. Evaluation Phase ---
            print(f"Gen {gen + 1}/{self.NUM_GENERATIONS} evaluating...", end="\r")

            for genotype in population:
                # Run a simulation episode for this genotype
                # We use headless mode for training efficiency regardless of config
                team_stats = self._run_single_episode(genotype, headless=True)

                # Calculate Team Novelty (Average of agents)
                team_novelty = 0
                for pos in team_stats["final_positions"]:
                    team_novelty += GU.calculate_euclidean_novelty(pos, archive)

                avg_novelty = team_novelty / len(team_stats["final_positions"])

                # Combined Fitness Calculation
                combined_score = team_stats["fitness"] + (avg_novelty * 10.0)

                result = {
                    "genotype": genotype,
                    "fitness": team_stats["fitness"],
                    "novelty": avg_novelty,
                    "combined": combined_score,
                    "final_positions": team_stats["final_positions"]
                }
                evaluated_results.append(result)

            # --- B. Archive Update ---
            # Sort by Novelty descending
            evaluated_results.sort(key=lambda x: x["novelty"], reverse=True)
            for i in range(min(self.N_ARCHIVE_ADD, len(evaluated_results))):
                for pos in evaluated_results[i]["final_positions"]:
                    archive.append(pos)

            # --- C. Statistics & Logging ---
            # Sort by Combined Fitness descending for selection
            evaluated_results.sort(key=lambda x: x["combined"], reverse=True)
            best_gen_result = evaluated_results[0]
            avg_score = sum(r["combined"] for r in evaluated_results) / self.POPULATION_SIZE

            # Update global best
            if best_result_global is None or best_gen_result["combined"] > best_result_global["combined"]:
                best_result_global = best_gen_result

            print(
                f"Gen {gen + 1} | Avg: {avg_score:.2f} | Best: {best_gen_result['combined']:.2f} (Fit: {best_gen_result['fitness']:.0f}, Nov: {best_gen_result['novelty']:.2f})")

            # --- D. Selection & Reproduction ---
            new_population = []

            # Elitism
            sorted_genomes = [r["genotype"] for r in evaluated_results]
            new_population.extend(sorted_genomes[:self.ELITISM_COUNT])

            # Breeding
            while len(new_population) < self.POPULATION_SIZE:
                parent1 = GU.tournament_selection_dict(evaluated_results, self.TOURNAMENT_SIZE)
                parent2 = GU.tournament_selection_dict(evaluated_results, self.TOURNAMENT_SIZE)

                child1, child2 = GU.crossover_one_point(parent1["genotype"], parent2["genotype"])

                GU.mutate_random_reset(child1, action_space, self.MUTATION_RATE)
                GU.mutate_random_reset(child2, action_space, self.MUTATION_RATE)

                new_population.append(child1)
                if len(new_population) < self.POPULATION_SIZE:
                    new_population.append(child2)

            population = new_population

        print(f"\n--- Evolution Complete. Best Combined Score: {best_result_global['combined']:.2f} ---")

        # Only replay visually if config_headless is False
        if not self.config_headless:
            self._replay_best_strategy(best_result_global["genotype"])
        else:
            print(">>> Replay skipped (Headless Mode) <<<")

    def _run_single_episode(self, genotype, headless=True):
        """
        Helper: Sets up a world, applies the genotype, and runs it until completion.
        Returns: Dictionary of collected statistics.
        """
        # 1. Reset the World
        # Instead of creating a new SimulatorMotor, we reset the existing one.
        # initialize_map acts as the "reset" by reloading the initial state.
        self.world.initialize_map(self.map_file_path)
        self.headless = headless

        # 2. Inject Brain (Genotype)
        for agent in self.world.agents:
            agent.genotype = genotype
            agent.learn_mode = True  # Use genes

        # 3. Execution Loop
        self.running = True
        time_limit = self.TIME_LIMIT
        time_step = self.TIME_PER_STEP_HEADLESS if headless else self.TIME_PER_STEP_VISUAL

        while self.running:
            if not self.headless:
                self.world.show_world()

            for agent in self.world.agents:
                agent.execute()

            time_limit -= 0.05  # decrement logic

            if self.world.solved or time_limit <= 0:
                self.running = False

            if not self.headless:
                time.sleep(time_step)

        # 4. Collect Stats
        total_reward = sum(a.reward for a in self.world.agents)
        final_positions = [a.position for a in self.world.agents]

        return {
            "fitness": total_reward,
            "final_positions": final_positions
        }

    def _replay_best_strategy(self, genotype):
        """ Replays the best genome visually. """
        print(">>> Replaying Best Strategy Visualized <<<")
        self._run_single_episode(genotype, headless=False)

    def shut_down(self):
        pass

    def save_state(self, file_name: str):
        pass