import random
import math


# --- SELECTION METHODS ---

def tournament_selection(population, k=3):
    """
    Selects one individual from the population using Tournament Selection.
    Arguments:
        population: List of objects (Agents) that have a 'combined_fitness' attribute.
        k: Tournament size.
    Returns:
        The best Agent from the random sample.
    """
    if len(population) < k:
        k = len(population)

    # Pick k random candidates
    candidates = random.sample(population, k)

    # Return the one with the highest combined fitness
    # Assumes agent has 'combined_fitness' attribute set
    best = max(candidates, key=lambda agent: agent.combined_fitness)
    return best

# Add this to GeneticUtils.py
def tournament_selection_dict(population_data, k=3):
    """ Selects best individual when population is a list of dictionaries """
    candidates = random.sample(population_data, min(k, len(population_data)))
    return max(candidates, key=lambda x: x["combined"])

def elitism_selection(population, n_elites):
    """
    Returns the top N best agents from the population to carry over unchanged.
    """
    # Sort by fitness descending
    sorted_pop = sorted(population, key=lambda agent: agent.combined_fitness, reverse=True)

    # Return top N genotypes (not the agent objects, just their DNA)
    return [agent.genotype[:] for agent in sorted_pop[:n_elites]]


# --- REPRODUCTION METHODS ---

def crossover_one_point(parent1_genes, parent2_genes):
    """
    Performs Single-Point Crossover.
    Returns: (child1_genes, child2_genes)
    """
    if len(parent1_genes) != len(parent2_genes):
        raise ValueError("Parents must have same genome length")

    # Choose a cut point
    point = random.randint(1, len(parent1_genes) - 1)

    # Create children
    child1 = parent1_genes[:point] + parent2_genes[point:]
    child2 = parent2_genes[:point] + parent1_genes[point:]

    return child1, child2


def mutate_random_reset(genotype, action_space, mutation_rate):
    """
    Mutates genes by resetting them to a new random action from the action_space.
    This modifies the list in-place.
    """
    for i in range(len(genotype)):
        if random.random() < mutation_rate:
            genotype[i] = random.choice(action_space)
    return genotype


# --- METRIC CALCULATIONS ---

def calculate_euclidean_novelty(agent_position, archive, k=15):
    """
    Calculates sparsity/novelty based on Euclidean distance to the k-nearest neighbors
    in the archive.

    Arguments:
        agent_position: Tuple (x, y)
        archive: List of Tuples [(x,y), (x,y)...]
        k: Number of neighbors to consider
    """
    if not archive:
        return 1.0  # Maximum novelty if archive is empty

    distances = []
    for past_pos in archive:
        dist = math.dist(agent_position, past_pos)
        distances.append(dist)

    distances.sort()

    # Get average distance to k nearest neighbors
    # If archive is smaller than k, take average of all
    neighbors = distances[:k]
    if not neighbors:
        return 0.0

    novelty_score = sum(neighbors) / len(neighbors)
    return novelty_score


def calculate_linear_combination(fitness, novelty, rho=0.5):
    """
    Combines Fitness and Novelty into a single score.
    You might need to normalize fitness/novelty before calling this if ranges differ wildly.
    """
    return (1 - rho) * fitness + rho * novelty