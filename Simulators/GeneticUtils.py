import random
import math


# --- CORE GENETIC OPERATIONS ---

def crossover(parent1_genes, parent2_genes):
    """ Performs single-point crossover. Returns two new child genotypes. """
    if len(parent1_genes) != len(parent2_genes):
        # Fallback for safety, though lengths should match
        point = random.randint(1, min(len(parent1_genes), len(parent2_genes)) - 1)
    else:
        point = random.randint(1, len(parent1_genes) - 1)

    child1 = parent1_genes[:point] + parent2_genes[point:]
    child2 = parent2_genes[:point] + parent1_genes[point:]
    return child1, child2


def mutate(genotype, action_space, mutation_rate):
    """ Randomly modifies genes in place. """
    for i in range(len(genotype)):
        if random.random() < mutation_rate:
            genotype[i] = random.choice(action_space)
    return genotype


def tournament_selection(population_results, k=3):
    """
    Selects a parent based on 'combined_fitness'.
    Input: List of dictionaries {'genotype': ..., 'combined': ...}
    """
    sample = random.sample(population_results, min(k, len(population_results)))
    # Return the data dict of the winner
    return max(sample, key=lambda x: x["combined"])


# --- NOVELTY & METRICS ---

def calculate_novelty(behavior, archive, k=15):
    """
    Calculates sparsity (novelty) of a behavior (x,y) against an archive.
    """
    if not archive:
        return 1.0  # Maximally novel if archive is empty

    # Calculate Euclidean distance to all points in archive
    distances = [math.dist(behavior, past_point) for past_point in archive]
    distances.sort()

    # Average distance to k-nearest neighbors
    k_nearest = distances[:k]
    if not k_nearest: return 0.0

    return sum(k_nearest) / len(k_nearest)