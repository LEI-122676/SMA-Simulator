import random
import math


def calculate_euclidean_novelty(position, archive, k=15):
    """
    Calculates the novelty score based on the average distance to the k-nearest neighbors in the archive.
    """
    if not archive:
        return 0.0

    distances = []
    x1, y1 = position

    for (x2, y2) in archive:
        dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        distances.append(dist)

    distances.sort()

    # Take the k nearest neighbors (or all if less than k)
    k_nearest = distances[:k]

    if not k_nearest:
        return 0.0

    avg_distance = sum(k_nearest) / len(k_nearest)
    return avg_distance


def tournament_selection_dict(evaluated_results, tournament_size):
    """
    Selects the best individual from a random sample of the population.
    Expects a list of dictionaries containing 'combined' score key.
    """
    candidates = random.sample(evaluated_results, tournament_size)
    # Return the one with the highest combined score
    best_candidate = max(candidates, key=lambda x: x["combined"])
    return best_candidate


def crossover_one_point(parent1_genes, parent2_genes):
    """
    Performs one-point crossover between two genotypes.
    Returns two child genotypes.
    """
    if len(parent1_genes) != len(parent2_genes):
        raise ValueError("Genotypes must be of equal length")

    length = len(parent1_genes)
    if length < 2:
        return list(parent1_genes), list(parent2_genes)

    # Pick a random crossover point
    cx_point = random.randint(1, length - 1)

    child1 = parent1_genes[:cx_point] + parent2_genes[cx_point:]
    child2 = parent2_genes[:cx_point] + parent1_genes[cx_point:]

    return child1, child2


def mutate_random_reset(genotype, action_space, mutation_rate):
    """
    Mutates a genotype in-place by resetting genes to random actions 
    based on the mutation rate.
    """
    for i in range(len(genotype)):
        if random.random() < mutation_rate:
            genotype[i] = random.choice(action_space)