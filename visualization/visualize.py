from Simulators.SimulatorMotor import SimulatorMotor

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import Worlds.CoopWorld as CoopWorld
import Worlds.ForagingWorld as ForagingWorld

def main():
    headless = True          # True == no graphics
    single_run = False        # True --> Debug 1 episode

    simple_farol = "Levels/simple_farol.txt"
    simple_foraging = "Levels/simple_foraging.txt"
    farol_level1 = "Levels/farol_level1.txt"
    farol_level2 = "Levels/farol_level2.txt"
    farol_level3 = "Levels/farol_level3.txt"
    farol_level4 = "Levels/farol_level4.txt"
    foraging_level1 = "Levels/foraging_level1.txt"
    foraging_level2 = "Levels/foraging_level2.txt"

    simulator = SimulatorMotor.create(
        farol_level1,
        headless=headless,
        single_run=single_run
    )

    # Configure run parameters
    simulator.POPULATION_SIZE = 40
    simulator.NUM_GENERATIONS = 20
    simulator.execute()

    # World dimensions
    width = simulator.world.width
    height = simulator.world.height

    # Data collected during evolution
    best_paths_per_gen = simulator.best_paths_per_gen
    avg_fitness_per_gen = simulator.avg_fitness_per_gen
    NUM_GENERATIONS = simulator.NUM_GENERATIONS

    # Visualizations
    heatmap_of_visited_areas(best_paths_per_gen, avg_fitness_per_gen, NUM_GENERATIONS, grid_size=(width, height))

    plot_best_paths(best_paths_per_gen, avg_fitness_per_gen, NUM_GENERATIONS, map_size=(width, height))


def heatmap_of_visited_areas(
    best_paths_per_gen,
    avg_fitness_per_gen=None,
    num_generations=None,
    grid_size=None,
    show=True
):
    if grid_size is None:
        raise ValueError("grid_size=(width, height) must be provided")

    width, height = grid_size
    heatmap = np.zeros((height, width))

    # Count visits (NO axis tricks here)
    for path in best_paths_per_gen:
        for x, y in path:
            xi = int(round(x))
            yi = int(round(y))

            if 0 <= xi < width and 0 <= yi < height:
                heatmap[yi, xi] += 1

    # Normalize heatmap values (0–1)
    if heatmap.max() > 0:
        heatmap /= heatmap.max()

    plt.figure(figsize=(8, 8))
    plt.imshow(heatmap, cmap="viridis")
    plt.gca().invert_yaxis()
    plt.colorbar(label="Normalized visit frequency")

    title = "Normalized Heatmap of Visited Areas"
    if num_generations is not None:
        title += f" ({num_generations} generations)"
    plt.title(title)

    plt.xlabel("X (normalized)")
    plt.ylabel("Y (normalized)")    
    plt.gca().invert_yaxis()

    plt.tight_layout()

    if show:
        plt.show()

    return heatmap

def plot_best_paths(best_paths_per_gen, avg_fitness_per_gen, NUM_GENERATIONS, map_size):
    width, height = map_size

    fig, ax = plt.subplots(figsize=(8, 8))
    colors = cm.viridis(np.linspace(0, 1, len(best_paths_per_gen)))

    plot_gens = [
        0,
        NUM_GENERATIONS // 2,
        NUM_GENERATIONS - 1
    ]

    for i in plot_gens:
        path = best_paths_per_gen[i]
        avg_fitness = avg_fitness_per_gen[i]

        x_vals = [p[0] / (width - 1) for p in path]
        y_vals = [1.0 - (p[1] / (height - 1)) for p in path]

        ax.plot(
            x_vals,
            y_vals,
            color=colors[i],
            label=f"Gen {i + 1} (Avg Fitness: {avg_fitness:.2f})",
            linewidth=2,
            alpha=0.8
        )

        ax.plot(x_vals[-1], y_vals[-1], 'x', color=colors[i], markersize=10)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")

    ax.set_title("Normalized Best Agent Paths")
    ax.set_xlabel("X (normalized)")
    ax.set_ylabel("Y (normalized)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()
