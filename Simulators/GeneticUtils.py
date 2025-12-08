import random


def jaccard_distance(set1, set2):
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
    if not archive:
        return 1.0

    distances = [jaccard_distance(current_behavior, b) for b in archive]
    distances.sort()
    return sum(distances[:k]) / k if len(distances) >= k else sum(distances) / len(distances)


def tournament_selection_dict(evaluated_results, tournament_size):
    """
    Selects the best individual from a random sample of the population.
    """
    candidates = random.sample(evaluated_results, tournament_size)
    best_candidate = max(candidates, key=lambda x: x["combined"])
    return best_candidate


def crossover_one_point(parent1_genes, parent2_genes):
    """
    Performs one-point crossover between two genotypes.
    """
    if len(parent1_genes) != len(parent2_genes):
        # Fallback if lengths differ (shouldn't happen in fixed topology)
        return list(parent1_genes), list(parent2_genes)

    length = len(parent1_genes)
    if length < 2:
        return list(parent1_genes), list(parent2_genes)

    cx_point = random.randint(1, length - 1)

    child1 = parent1_genes[:cx_point] + parent2_genes[cx_point:]
    child2 = parent2_genes[:cx_point] + parent1_genes[cx_point:]

    return child1, child2


def mutate_weights_gaussian(genotype, mutation_rate, sigma=0.1):
    """
    Mutates a list of floats (weights) by adding Gaussian noise.
    Used for Neuroevolution.
    """
    for i in range(len(genotype)):
        if random.random() < mutation_rate:
            # Add noise
            genotype[i] += random.gauss(0, sigma)
            # Clamp weights to keep them stable (optional, but good practice)
            genotype[i] = max(-2.0, min(2.0, genotype[i]))


def mutate_random_reset(genotype, action_space, mutation_rate):
    """
    Legacy mutation for Discrete Actions.
    """
    for i in range(len(genotype)):
        if random.random() < mutation_rate:
            genotype[i] = random.choice(action_space)