import time
import random
import pickle
import numpy as np

# Specific imports for factory functions
from NeuralNetworks.NeuralNetworkCoop import create_coop_network
from NeuralNetworks.NeuralNetworkForaging import create_foraging_network

import GeneticUtils as GU

from Actions.Action import Action

from Worlds.CoopWorld import CoopWorld
from Worlds.ForagingWorld import ForagingWorld
from Simulators.Simulator import Simulator
from Simulators.Utilities import read_matrix_file_with_metadata


class SimulatorMotor(Simulator):
    POPULATION_SIZE = 80
    NUM_GENERATIONS = 50
    MUTATION_RATE = 0.05
    MUTATION_SIGMA = 0.5
    TOURNAMENT_SIZE = 4
    N_ARCHIVE_ADD = 3
    ELITISM_COUNT = 2

    P = 0.8

    TIME_LIMIT = 200
    TIME_PER_STEP_HEADLESS = 0.0
    TIME_PER_STEP_VISUAL = 0.05
    SAVE_FILE = "evolution_state.pkl"

    def __init__(self, world, map_file_path, headless=False, single_run=False):
        self.world = world
        self.map_file_path = map_file_path
        self.running = True
        self.config_headless = headless
        self.single_run = single_run
        self.population = []
        self.archive = []
        self.best_result_global = None
        self.current_generation = 0
        self.best_paths_per_gen = []
        self.avg_fitness_per_gen = []
        self.best_behaviors = []

        # Init Dummy NN to calculate genome size
        if isinstance(self.world, CoopWorld):
            dummy_nn = create_coop_network()
            print("Detected CoopWorld. Using NeuralNetworkCoop.")
        else:
            dummy_nn = create_foraging_network()
            print("Detected ForagingWorld. Using NeuralNetworkForaging.")

        self.genome_size = dummy_nn.compute_num_weights()
        print(f"Network Inputs: {dummy_nn.get_input_size()} | Weights: {self.genome_size}")

    @staticmethod
    def create(matrix_file, headless=False, single_run=False):
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
            world.initialize_map(matrix_file)

        return SimulatorMotor(world, matrix_file, headless, single_run)

    def test(self):
        print("--- TESTING MODE: Loading Best Genome ---")
        try:
            with open(self.SAVE_FILE, "rb") as f:
                state = pickle.load(f)

            best_result = state.get("best_result")
            if not best_result:
                print("No best result found in save file.")
                return

            print(f"Loaded Genome. Best Training Score: {best_result['combined']:.2f}")

            # Use visual replay
            self._run_single_episode(best_result["genotype"], headless=False)

        except FileNotFoundError:
            print(f"Save file {self.SAVE_FILE} not found. Run training first.")
        except Exception as e:
            print(f"Error loading state: {e}")

    def execute(self):
        print(f"--- Starting Evolutionary Process ---")
        if not self.population:
            for _ in range(self.POPULATION_SIZE):
                weights = np.random.uniform(-1, 1, self.genome_size).tolist()
                self.population.append(weights)

        # Main Loop
        for gen in range(self.current_generation, self.NUM_GENERATIONS):
            if not self.running: break
            self.current_generation = gen
            evaluated_results = []
            print(f"Gen {gen + 1}/{self.NUM_GENERATIONS} evaluating...", end="\r")

            for genotype in self.population:
                team_stats = self._run_single_episode(genotype, headless=True)

                # Novelty Calculation
                team_novelty = 0
                archive_sets = [set(p) for p in self.archive]
                for pos in team_stats["final_positions"]:
                    team_novelty += GU.compute_novelty(set(pos), archive_sets)
                avg_novelty = team_novelty / len(team_stats["final_positions"]) if team_stats["final_positions"] else 0

                combined_score = (self.P * team_stats["fitness"]) + ((1 - self.P) * (avg_novelty * 100.0))

                result = {
                    "genotype": genotype,
                    "fitness": team_stats["fitness"],
                    "novelty": avg_novelty,
                    "combined": combined_score,
                    "final_positions": team_stats["final_positions"]
                }
                evaluated_results.append(result)

            # Archive Logic
            evaluated_results.sort(key=lambda x: x["novelty"], reverse=True)
            for i in range(min(self.N_ARCHIVE_ADD, len(evaluated_results))):
                for pos in evaluated_results[i]["final_positions"]:
                    self.archive.append(pos)

            evaluated_results.sort(key=lambda x: x["combined"], reverse=True)
            best_gen_result = evaluated_results[0]

            if self.best_result_global is None or best_gen_result["combined"] > self.best_result_global["combined"]:
                self.best_result_global = best_gen_result

            avg = sum(r["combined"] for r in evaluated_results) / self.POPULATION_SIZE

            # --- RESTORED LOGGING ---
            print(
                f"Gen {gen + 1} | Avg: {avg:.2f} | Best: {best_gen_result['combined']:.2f} (Fit: {best_gen_result['fitness']:.0f}, Nov: {best_gen_result['novelty']:.2f})")

            # Selection
            new_population = []
            sorted_genomes = [r["genotype"] for r in evaluated_results]
            new_population.extend(sorted_genomes[:self.ELITISM_COUNT])

            while len(new_population) < self.POPULATION_SIZE:
                p1 = GU.tournament_selection_dict(evaluated_results, self.TOURNAMENT_SIZE)
                p2 = GU.tournament_selection_dict(evaluated_results, self.TOURNAMENT_SIZE)
                c1, c2 = GU.crossover_one_point(p1["genotype"], p2["genotype"])
                GU.mutate_weights_gaussian(c1, self.MUTATION_RATE, self.MUTATION_SIGMA)
                GU.mutate_weights_gaussian(c2, self.MUTATION_RATE, self.MUTATION_SIGMA)
                new_population.append(c1)
                if len(new_population) < self.POPULATION_SIZE: new_population.append(c2)

            self.population = new_population

        self._shut_down()

    def _run_single_episode(self, genotype, headless=True):
        self.world.initialize_map(self.map_file_path)

        for agent in self.world.agents:
            # Instantiate correct NN
            if isinstance(self.world, CoopWorld):
                nn = create_coop_network()
            else:
                nn = create_foraging_network()

            nn.load_weights(genotype)
            agent.nn = nn
            agent.learn_mode = True

        episode_running = True
        time_limit = self.TIME_LIMIT
        game_steps = []

        while episode_running and self.running:
            if not headless:
                game_steps.append(self.world.show_world())

            agents = self.world.agents[:]
            random.shuffle(agents)

            for agent in agents:
                agent.execute()

            if self.world.is_over():
                episode_running = False

            time_limit -= 0.05
            if time_limit <= 0:
                episode_running = False

        if not headless:
            for step in game_steps:
                print(step)
                print("\n")
                time.sleep(self.TIME_PER_STEP_VISUAL)

        total_reward = sum(a.reward for a in self.world.agents)
        return {
            "fitness": total_reward,
            "final_positions": [a.position for a in self.world.agents]
        }

    def _shut_down(self):
        print(f"\n--- Evolution Complete. Best: {self.best_result_global['combined']:.2f} ---")
        self._save_state()
        if not self.config_headless and self.best_result_global:
            self._replay_best_strategy(self.best_result_global["genotype"])
        self.running = False
        print("[System] Simulation shut down.")

    def _replay_best_strategy(self, genotype):
        print(">>> Replaying Best Strategy Visualized <<<")
        self._run_single_episode(genotype, headless=False)

    def _save_state(self):
        state = {
            "population": self.population,
            "archive": self.archive,
            "best_result": self.best_result_global,
            "generation": self.current_generation
        }
        try:
            with open(self.SAVE_FILE, "wb") as f:
                pickle.dump(state, f)
        except Exception:
            pass