import time
import random
import pickle
import numpy as np
from pathlib import Path
from . import GeneticUtils as GU

# Specific imports for factory functions
from NeuralNetworks.NeuralNetworkCoop import create_coop_network
from NeuralNetworks.NeuralNetworkForaging import create_foraging_network

from Actions.Action import Action

from Worlds.CoopWorld import CoopWorld
from Worlds.ForagingWorld import ForagingWorld
from Simulators.Simulator import Simulator
from Simulators.Utilities import read_matrix_file_with_metadata

from Items.ChickenCoop import ChickenCoop
from Actions.Direction import Direction
from Items.Nest import Nest
from Items.Egg import Egg


class SimulatorMotor(Simulator):
    POPULATION_SIZE = 100
    NUM_GENERATIONS = 50
    MUTATION_RATE = 0.05
    MUTATION_SIGMA = 0.5
    TOURNAMENT_SIZE = 4
    N_ARCHIVE_ADD = 1
    ELITISM_COUNT = 2

    P = 0.75

    TIME_LIMIT = 200
    TIME_PER_STEP_HEADLESS = 0.0
    TIME_PER_STEP_VISUAL = 0.05
    SAVE_FILE = "evolution_state.pkl"

    def __init__(self, world, map_file_path, headless=False, single_run=False):
        """
        Initialize with a 'template' world, the file path to recreate it,
        and a headless configuration.
        """
        self.world = world
        self.map_file_path = map_file_path
        self.running = True

        # Configuration for the simulation run
        self.config_headless = headless
        self.single_run = single_run

        # Evolutionary State
        self.population = []
        self.archive = []
        self.best_result_global = None
        self.current_generation = 0
        # History collected per generation
        self.best_paths_per_gen = []  # representative best path per generation (list of (x,y))
        self.avg_fitness_per_gen = []  # average combined score per generation
        self.best_behaviors = []  # set of visited positions for best agent per generation

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

    def test(self, map_file=None):
        """
        Loads the best genome from the save file and replays it.
        Args:
            map_file (str, optional): Overrides the map to test on.
                                      If None, uses the map from the save file.
        """
        print("--- TESTING MODE: Loading Best Genome ---")
        try:
            with open(self.SAVE_FILE, "rb") as f:
                state = pickle.load(f)

            best_result = state.get("best_result")
            if not best_result:
                print("No best result found in save file.")
                return

            print(f"Loaded Genome. Best Training Score: {best_result['combined']:.2f}")

            # Determine which map to use
            target_map = map_file if map_file else state.get("map", self.map_file_path)

            # Check if map changed
            if target_map != self.map_file_path:
                print(f"Switching map from {self.map_file_path} to {target_map}")
                self.map_file_path = target_map

                # Re-initialize the world with the new map
                # This ensures the world dimensions and object lists match the new file
                try:
                    self.world.initialize_map(self.map_file_path)
                except ValueError as e:
                    # If the world type doesn't match the map (e.g. CoopWorld vs Foraging map)
                    print(f"Error initializing map: {e}")
                    print("It seems you are trying to load a map incompatible with the current World type.")
                    return

            print(f"Testing on Map: {self.map_file_path}")

            # Use visual replay
            self._run_single_episode(best_result["genotype"], headless=False)

        except FileNotFoundError:
            print(f"Save file {self.SAVE_FILE} not found. Run training first.")
        except Exception as e:
            print(f"Error loading state: {e}")

    def execute(self, method="evolutionary"):
        # ... (Same as provided in your prompt)
        if method == "evolutionary":
            self.evolutionary()
        if method == "fixed_policy":
            self.fixed_policy()

    def evolutionary(self):
        # ... (Same as provided in your prompt)
        print(f"--- Starting Evolutionary Process ---")
        if not self.population:
            for _ in range(self.POPULATION_SIZE):
                weights = np.random.uniform(-1, 1, self.genome_size).tolist()
                self.population.append(weights)

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
                    "final_positions": team_stats["final_positions"],
                    "paths": team_stats.get("paths", [])
                }
                evaluated_results.append(result)

            evaluated_results.sort(key=lambda x: x["novelty"], reverse=True)
            for i in range(min(self.N_ARCHIVE_ADD, len(evaluated_results))):
                for pos in evaluated_results[i]["final_positions"]:
                    self.archive.append(pos)

            evaluated_results.sort(key=lambda x: x["combined"], reverse=True)
            best_gen_result = evaluated_results[0]
            avg_score = sum(r["combined"] for r in evaluated_results) / self.POPULATION_SIZE

            best_paths_info = best_gen_result.get("paths", [])
            if best_paths_info and isinstance(best_paths_info, list):
                rep_path = list(best_paths_info[0]) if len(best_paths_info) > 0 else []
            else:
                rep_path = best_gen_result.get("final_positions", [])

            self.best_paths_per_gen.append(rep_path)
            self.avg_fitness_per_gen.append(avg_score)

            try:
                path_set = set(tuple(p) for p in rep_path)
                self.best_behaviors.append(path_set)
            except Exception:
                self.best_behaviors.append(set())

            if self.best_result_global is None or best_gen_result["combined"] > self.best_result_global["combined"]:
                self.best_result_global = best_gen_result

            print(
                f"Gen {gen + 1} | Avg: {avg_score:.2f} | Best: {best_gen_result['combined']:.2f} (Fit: {best_gen_result['fitness']:.0f}, Nov: {best_gen_result['novelty']:.2f})")

            new_population = []
            sorted_genomes = [r["genotype"] for r in evaluated_results]
            new_population.extend(sorted_genomes[:self.ELITISM_COUNT])

            while len(new_population) < self.POPULATION_SIZE:
                parent1 = GU.tournament_selection_dict(evaluated_results, self.TOURNAMENT_SIZE)
                parent2 = GU.tournament_selection_dict(evaluated_results, self.TOURNAMENT_SIZE)
                child1, child2 = GU.crossover_one_point(parent1["genotype"], parent2["genotype"])
                GU.mutate_weights_gaussian(child1, self.MUTATION_RATE, self.MUTATION_SIGMA)
                GU.mutate_weights_gaussian(child2, self.MUTATION_RATE, self.MUTATION_SIGMA)
                new_population.append(child1)
                if len(new_population) < self.POPULATION_SIZE:
                    new_population.append(child2)

            self.population = new_population

        self._shut_down()

    def fixed_policy(self):
        # ... (Same as provided in your prompt)
        print("--- FIXED POLICY MODE ---")
        self.world.initialize_map(self.map_file_path)

        episode_running = True
        time_limit = self.TIME_LIMIT

        while episode_running and self.running:
            if not self.config_headless:
                print(self.world.show_world())
                print("\n")

            agents = self.world.agents[:]
            random.shuffle(agents)

            for agent in agents:
                action = None
                if isinstance(self.world, CoopWorld):
                    # Move towards the Farol
                    chickenCoop = self.world.chicken_coop
                    if chickenCoop.position is not None:
                        action = ChickenCoop.get_action(chickenCoop.position, agent.position)
                else:
                    # Foraging Logic
                    try:
                        agent.sensor.max_range = self.world.width + self.world.height
                        observation = self.world.observation_for(agent)
                        wanted_types = (Nest,) if agent.inventory else (Egg,)

                        seen = []
                        for dir_name, (dist, obj_type) in observation.rays.items():
                            if obj_type is None:
                                continue
                            if obj_type in wanted_types:
                                seen.append((dir_name, dist))

                        if not seen:
                            action = Action.random_action()
                        else:
                            seen.sort(key=lambda t: t[1])
                            dir_name = seen[0][0]
                            dir_vec = None
                            for d in Direction:
                                if d.name.replace('_', '').upper() == dir_name.replace('_', '').upper():
                                    dir_vec = d.value
                                    break

                            if dir_vec is None:
                                action = Action.random_action()
                            else:
                                dx, dy = dir_vec
                                if dx != 0 and dy != 0:
                                    if random.random() < 0.5:
                                        dy = 0
                                    else:
                                        dx = 0
                                action_by_vec = {a.value: a for a in Action}
                                action = action_by_vec.get((dx, dy), Action.random_action())
                    except Exception as e:
                        print(f"Sensor Logic Error: {e}")
                        action = Action.random_action()

                if action is not None:
                    try:
                        self.world.act(action, agent)
                    except Exception:
                        pass
                    try:
                        agent.step_index += 1
                        agent.behavior.add(agent.position)
                        agent.path.append(agent.position)
                        agent.update_goal_vector()
                    except Exception:
                        pass

            if self.world.is_over():
                episode_running = False

            time_limit -= 1
            if time_limit <= 0:
                episode_running = False

            if not self.config_headless:
                time.sleep(self.TIME_PER_STEP_VISUAL)

        print("--- Fixed Policy Complete ---")
        try:
            if len(self.world.agents) > 0:
                collected_paths = [list(agent.path) for agent in self.world.agents]
                self.best_paths_per_gen = collected_paths
                avg_fitness = sum(getattr(agent, 'reward', 0) for agent in self.world.agents) / len(self.world.agents)
                self.avg_fitness_per_gen = [avg_fitness]
                self.best_behaviors = [set(tuple(p) for p in agent.path) for agent in self.world.agents]
                self.current_generation = 0
                self.best_result_global = {
                    'combined': avg_fitness,
                    'fitness': sum(getattr(agent, 'reward', 0) for agent in self.world.agents),
                    'final_positions': [tuple(agent.position) for agent in self.world.agents],
                    'genotype': None
                }
            self._save_state()
        except Exception as e:
            print(f"[Warning] failed to record fixed_policy paths: {e}")

    def _get_direction(self, from_pos, to_pos):
        dx = to_pos[0] - from_pos[0]
        dy = to_pos[1] - from_pos[1]

        if abs(dx) > abs(dy):
            return (1, 0) if dx > 0 else (-1, 0)
        else:
            return (0, 1) if dy > 0 else (0, -1)

    def _run_single_episode(self, genotype, headless=True):
        self.world.initialize_map(self.map_file_path)

        for agent in self.world.agents:
            if isinstance(self.world, CoopWorld):
                nn = create_coop_network()
            else:
                nn = create_foraging_network()

            # Ensure we don't crash if the genotype is None (fixed policy mode)
            if genotype is not None:
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
            "final_positions": [a.position for a in self.world.agents],
            "paths": [a.path for a in self.world.agents]
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
        try:
            map_path = str(Path(self.map_file_path).resolve()) if self.map_file_path else None
        except Exception:
            map_path = self.map_file_path

        state = {
            "map": map_path,
            "population": self.population,
            "archive": self.archive,
            "best_result": self.best_result_global,
            "generation": self.current_generation,
            "paths": [a.path for a in self.world.agents],
            "best_paths_per_gen": self.best_paths_per_gen,
            "avg_fitness_per_gen": self.avg_fitness_per_gen,
            "best_behaviors": [list(b) for b in self.best_behaviors]
        }
        try:
            with open(self.SAVE_FILE, "wb") as f:
                pickle.dump(state, f)
            print(f"\n[System] State saved successfully to {self.SAVE_FILE}")
        except Exception as e:
            print(f"\n[System] Error saving state: {e}")

    def get_history(self):
        return {
            "best_paths_per_gen": self.best_paths_per_gen,
            "avg_fitness_per_gen": self.avg_fitness_per_gen,
            "best_behaviors": self.best_behaviors,
            "final_population": self.population,
        }