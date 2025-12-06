import random
import math


def jaccard_distance(set1, set2):  # BC
    """
    Calculates the Jaccard distance between two sets.
    Distance = 1 - (Intersection / Union)
    """
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return 1 - intersection / union if union != 0 else 0

def compute_novelty(current_behavior, archive, k=5):
    """
    Calculates novelty based on Jaccard distance to the k-nearest neighbors in the archive.
    """
    # Handle the empty archive case
    if not archive:
        # The first item is, by definition, maximally novel
        return 1.0

    distances = [jaccard_distance(current_behavior, b) for b in archive]
    distances.sort()

    # Your original logic is now safe because we know len(distances) > 0
    return sum(distances[:k]) / k if len(distances) >= k else sum(distances) / len(distances)


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