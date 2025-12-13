import random

from Agents.Agent import Agent

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

    try:
        with open(file_name, "r") as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue

                if line.startswith("#"):
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

        return matrix

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_name}' does not exist")

def read_agent_config(file_name: str) -> dict:
    config = {}
    try:
        with open(file_name, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ValueError(f"Invalid line in config: {line}")
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Agent config file '{file_name}' does not exist")


def heatmap_of_visited_areas(population, NUM_GENERATIONS):
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns

    heatmap = np.zeros((100, 100))
    final_visited_maps = [agent.behavior for agent in population]

    for visited in final_visited_maps:
        for (x, y) in visited:
            heatmap[y][x] += 1

    # --- Plot and Invert Heatmap ---
    plt.figure(figsize=(10, 10))
    # Create the heatmap on a specific axes object
    ax = sns.heatmap(heatmap, cmap="YlGnBu")

    tick_locations = np.arange(0, 101, 20)

    ax.set_xticks(tick_locations)
    ax.set_yticks(tick_locations)
    ax.set_xticklabels(tick_locations)
    ax.set_yticklabels(tick_locations)

    # Invert the y-axis to match the path plot
    # This puts y=99 (start) at the TOP-LEFT
    ax.invert_yaxis()
    #ax.set_xlim(-1, 100)
    #ax.set_ylim(-1, 100)
    # ---------------------------------

    # --- Add Key and Treasure Labels to Heatmap ---
    env_for_labels = Map()
    for key in env_for_labels.keys:
        # Text labels use data coordinates, so they will
        # be placed correctly on the inverted axis.
        plt.text(key.x + 0.5, key.y + 0.5, key.name, color='black', fontsize=8, ha='center', va='center', fontweight='bold')

    for treasure in env_for_labels.treasures:
        plt.text(treasure.x + 0.5, treasure.y + 0.5, treasure.name, color='white', fontsize=8, ha='center', va='center', fontweight='bold')
    # ----------------------------------------------

    plt.title(f"Heatmap of Visited Areas by Final Population (Gen {NUM_GENERATIONS})")
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.show()
    
def plot_best_paths(best_paths_per_gen, avg_fitness_per_gen, NUM_GENERATIONS):
        
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm

    fig, ax = plt.subplots(figsize=(10, 10))
    colors = cm.rainbow(np.linspace(0, 1, len(best_paths_per_gen)))

    # --- Add Key and Treasure Labels ---
    env_for_labels = Map()
    for key in env_for_labels.keys:
        ax.text(key.x, key.y, key.name, color='black', fontsize=9, ha='center', va='center', fontweight='bold')
    for treasure in env_for_labels.treasures:
        ax.text(treasure.x, treasure.y, treasure.name, color='purple', fontsize=9, ha='center', va='center', fontweight='bold')
    # -----------------------------------

    # Plot paths
    plot_gens = [0, NUM_GENERATIONS // 2, NUM_GENERATIONS - 1]
    for i in plot_gens:
        path = best_paths_per_gen[i]
        avg_fitness = avg_fitness_per_gen[i] # Get the avg combined fitness
        x_vals = [p[0] for p in path]
        y_vals = [p[1] for p in path]
        ax.plot(x_vals, y_vals, color=colors[i], label=f"Gen {i+1} (Avg Fitness: {avg_fitness:.2f})", alpha=0.7)
        ax.plot(x_vals[-1], y_vals[-1], 'x', color=colors[i], markersize=10, markeredgewidth=2)

    ax.set_xlim(-1, 100)
    ax.set_ylim(-1, 100)
    ax.set_title("Best Agent Paths with Key (K) and Treasure (T) Locations")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend()
    plt.grid(True)
    plt.show()