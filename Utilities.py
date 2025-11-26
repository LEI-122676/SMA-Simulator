import random

from Agent.Agent import Agent
import Actions.Direction as D

def jaccard_distance(set1, set2):
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return 1 - intersection / union if union != 0 else 0

def compute_novelty(current_behavior, archive, k=5):
    # Handle the empty archive case
    if not archive:
        # The first item is, by definition, maximally novel
        return 1.0

    distances = [jaccard_distance(current_behavior, b) for b in archive]
    distances.sort()

    # Your original logic is now safe because we know len(distances) > 0
    return sum(distances[:k]) / k if len(distances) >= k else sum(distances) / len(distances)

def crossover(parent1, parent2):
    """Performs single-point crossover on two parent genotypes."""
    point = random.randint(1, len(parent1.genotype) - 1)
    child1_geno = parent1.genotype[:point] + parent2.genotype[point:]
    child2_geno = parent2.genotype[:point] + parent1.genotype[point:]
    return Agent(child1_geno), Agent(child2_geno)

def multi_point_crossover(parent1, parent2):
    points = sorted(random.sample(range(1, len(parent1.genotype) - 1), 2))
    child1_geno = (parent1.genotype[:points[0]] +
                    parent2.genotype[points[0]:points[1]] +
                    parent1.genotype[points[1]:])
    child2_geno = (parent2.genotype[:points[0]] +
                    parent1.genotype[points[0]:points[1]] +
                    parent2.genotype[points[1]:])
    return Agent(child1_geno), Agent(child2_geno)

def select_parent(population, tournament_size):
    """Selects a parent using tournament selection based on *combined_fitness*."""
    tournament = random.sample(population, tournament_size)
    tournament.sort(key=lambda x: x.combined_fitness, reverse=True)
    return tournament[0]

def run_evolution(self):

    # --- EA Hyperparameters ---
    POPULATION_SIZE = 50
    NUM_GENERATIONS = 25
    MUTATION_RATE = 0.01
    TOURNAMENT_SIZE = 3
    N_ARCHIVE_ADD = 5  # Add top 5 most novel agents to archive each gen

    # --- Initialization ---
    archive = []
    population = [Agent() for _ in range(POPULATION_SIZE)]
    avg_fitness_per_gen = []
    best_paths_per_gen = []

    print("Starting evolution...")

    # --- Generational Loop ---
    for gen in range(NUM_GENERATIONS):
        total_fitness = 0

        # 1. Evaluate Population
        for agent in population:
            agent.run_simulation()

            # --- Calculate and combine scores ---
            novelty_score = compute_novelty(agent.behavior, archive)
            objective_score = agent.calculate_objective_fitness()

            # Combine the scores.
            # You might need to add a weight, e.g.:
            novelty_weight = 1000  # Make novelty competitive with fitness
            agent.combined_fitness = (novelty_score * novelty_weight) + objective_score

            # agent.combined_fitness = novelty_score #+ objective_score

            total_fitness += agent.combined_fitness

        # 2. Sort population by *combined_fitness*
        population.sort(key=lambda x: x.combined_fitness, reverse=True)

        # 3. Log results for this generation
        avg_fitness = total_fitness / POPULATION_SIZE
        avg_fitness_per_gen.append(avg_fitness)
        best_paths_per_gen.append(population[0].path)

        # Get the top agent's individual scores for logging
        best_nov = compute_novelty(population[0].behavior, archive)
        best_obj = population[0].calculate_objective_fitness()

        print(
            f"Gen {gen + 1}/{NUM_GENERATIONS} | Avg Combined: {avg_fitness:.2f} | Best Combined: {population[0].combined_fitness:.2f} (Nov: {best_nov:.2f}, Obj: {best_obj})")

        # 4. Update archive with the most novel behaviors (from this gen)
        #    We still update the archive based on *pure novelty*

        # Sort by novelty just for archive update
        population.sort(key=lambda x: compute_novelty(x.behavior, archive), reverse=True)
        for i in range(N_ARCHIVE_ADD):
            archive.append(population[i].behavior)

        # Re-sort by combined fitness for breeding
        population.sort(key=lambda x: x.combined_fitness, reverse=True)

        # 5. Create new generation (Selection, Crossover, Mutation)
        new_population = []

        n_elite = POPULATION_SIZE // 10
        new_population.extend(population[:n_elite])

        while len(new_population) < POPULATION_SIZE:
            parent1 = select_parent(population, TOURNAMENT_SIZE)  # This now uses combined_fitness
            parent2 = select_parent(population, TOURNAMENT_SIZE)

            child1, child2 = crossover(parent1, parent2)

            child1.mutate(MUTATION_RATE)
            child2.mutate(MUTATION_RATE)

            new_population.append(child1)
            if len(new_population) < POPULATION_SIZE:
                new_population.append(child2)

        population = new_population

    print("Evolution complete.")

    # Convenience wrappers expected by Simulator
    def run_simulation(self):
        self.run()

def get_farol_vector(farol, agente):
    farol_position = farol.lightHouse.position
    agente_position = agente.position
    
    distance = ((farol_position[0] - agente_position[0]), (farol_position[1] - agente_position[1]))
    vector = [0,0]
    if farol_position[0] < agente_position[0]:
        vector = (-1, 0)  # West
    elif farol_position[0] > agente_position[0]:
        vector = (1, 0)   # East
    else:
        if farol_position[1] > agente_position[1]:
            vector = (0, 1)  # South
        elif farol_position[1] < agente_position[1]:
            vector = (0, -1)  # North
        else:
            vector = (0, 0)  # Same position
    
    return vector

def read_file_parameters(allowed_params, file_name):
    
    
    # TODO : NOVO FORMATO DE CONFIGURAÇÃO EM MATRIZ

    allowed = {p: None for p in allowed_params}  # Dict of allowed keys

    try:
        with open(file_name, "r") as f:
            for line in f:

                # Clean and skip empty/comment lines
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ValueError(f"Invalid line (no '='): {line}")

                key, value = line.split("=", 1)
                key = key.strip()

                if key not in allowed:
                    raise ValueError(f"Unexpected parameter in file: '{key}'")

                value = value.strip()

                # Try to convert to int or float
                if value.isdigit():
                    value = int(value)
                else:
                    try:
                        value = float(value)
                    except ValueError:
                        pass  # keep as string

                allowed[key] = value

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_name}' does not exist")

    # Check for missing allowed parameters
    missing = [k for k, v in allowed.items() if v is None]
    if missing:
        raise ValueError(f"Missing required parameters: {missing}")

    return allowed

def read_matrix_file_with_metadata(file_name):
    ALLOWED_CHARS = {'.', 'E', 'N', 'S', 'W', 'F', 'C'}
    matrix = []
    metadata = {}

    try:
        with open(file_name, "r") as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue

                if line.startswith("#"):
                    # Metadata line
                    if "=" in line:
                        key, value = line[1:].split("=", 1)
                        metadata[key.strip()] = value.strip()
                    continue

                # Validate characters
                for char in line:
                    if char not in ALLOWED_CHARS:
                        raise ValueError(
                            f"Invalid character '{char}' on line {line_number}"
                        )

                matrix.append(list(line))

        if not matrix:
            raise ValueError("Matrix is empty")

        # Ensure all rows are same length
        row_length = len(matrix[0])
        for i, row in enumerate(matrix, start=1):
            if len(row) != row_length:
                raise ValueError(f"Row {i} has length {len(row)}, expected {row_length}")

        return matrix, metadata

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_name}' does not exist")
