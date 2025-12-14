#!/usr/bin/env python3
"""Simple visualization runner for SMA-Simulator.

Produces three figures from a real SimulatorMotor run (or a saved history):
- Heatmap of visited tiles (aggregated from best behaviors per generation)
- Overlay of representative best paths (sampled generations)
- Average combined fitness per generation

The script prefers saving PNGs to an output directory for headless runs.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from typing import List, Optional

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import Rectangle
import seaborn as sns
from matplotlib import patheffects as path_effects

from Simulators.SimulatorMotor import SimulatorMotor
from Worlds.CoopWorld import CoopWorld


from Items.Wall import Wall
from Items.Egg import Egg
from Items.Nest import Nest
from Items.Stone import Stone
from Items.ChickenCoop import ChickenCoop

def parse_start_positions(map_file_path: Optional[str]) -> List[tuple]:
    """Read the map file and return a list of coordinates where 'C' appears.

    Returns list of (x,y). If file is None or unreadable, returns empty list.
    """
    if not map_file_path:
        return []
    try:
        starts = []
        with open(map_file_path, "r") as f:
            for y, line in enumerate(f.readlines()):
                for x, ch in enumerate(line.rstrip("\n")):
                    if ch == "C":
                        starts.append((x, y))
        return starts
    except Exception:
        return []


def run_evolution(map_file: str, pop: int, gens: int, headless: bool) -> SimulatorMotor:
    motor = SimulatorMotor.create(map_file, headless=headless, single_run=False)
    motor.POPULATION_SIZE = pop
    motor.NUM_GENERATIONS = gens
    motor.execute()
    return motor


def save_or_show(fig, outdir: Optional[Path], name: str):
    if outdir:
        path = outdir / f"{name}.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"Saved {path}")
    else:
        fig.show()


def plot_heatmap(best_behaviors: List[set], env, generations: int, outdir: Optional[Path], start_positions=None, goal_positions=None):
    width, height = env.width, env.height
    heatmap = np.zeros((height, width), dtype=float)

    for beh in best_behaviors:
        for (x, y) in beh:
            if 0 <= x < width and 0 <= y < height:
                heatmap[int(y), int(x)] += 1

    fig, ax = plt.subplots(figsize=(6, 6))

    sns.heatmap(heatmap, ax=ax, cmap="YlOrRd", cbar_kws={"label": "visits"}, zorder=0)
    ax.set_axisbelow(False)
    ax.invert_yaxis()
    ax.set_title(f"Visited Areas Heatmap — {generations} gens")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    for y in range(height):
        for x in range(width):
            tile = env.map[y][x]
            if tile is None:
                continue
            if isinstance(tile, Wall):
                rect = Rectangle((x - 0.5, y - 0.5), 1, 1, facecolor="#888888", edgecolor="#444444", linewidth=0.5, zorder=6)
                ax.add_patch(rect)
            if isinstance(tile, Egg):
                t = ax.text(x + 0.0, y + 0.0, "E", color="black", fontsize=8, weight="bold", ha="center", va="center", zorder=12)
                t.set_path_effects([path_effects.Stroke(linewidth=1.5, foreground='white'), path_effects.Normal()])
            elif isinstance(tile, Nest):
                t = ax.text(x + 0.0, y + 0.0, "N", color="purple", fontsize=8, weight="bold", ha="center", va="center", zorder=12)
                t.set_path_effects([path_effects.Stroke(linewidth=1.5, foreground='white'), path_effects.Normal()])
            elif isinstance(tile, Stone):
                t = ax.text(x + 0.0, y + 0.0, "S", color="saddlebrown", fontsize=8, weight="bold", ha="center", va="center", zorder=12)
                t.set_path_effects([path_effects.Stroke(linewidth=1.5, foreground='white'), path_effects.Normal()])
            elif isinstance(tile, ChickenCoop):
                t = ax.text(x + 0.0, y + 0.0, "F", color="blue", fontsize=10, weight="bold", ha="center", va="center", zorder=12)
                t.set_path_effects([path_effects.Stroke(linewidth=1.5, foreground='white'), path_effects.Normal()])

    if start_positions:
        sx = [p[0] for p in start_positions]
        sy = [p[1] for p in start_positions]
        ax.scatter(sx, sy, marker="^", color="green", s=120, edgecolor="k", label="start(s)", zorder=5)

    if goal_positions:
        if isinstance(goal_positions, tuple):
            goal_positions = [goal_positions]
        gx = [p[0] for p in goal_positions]
        gy = [p[1] for p in goal_positions]
        ax.scatter(gx, gy, marker="s", color="red", s=140, edgecolor="k", label="goal(s)", zorder=5)

    if start_positions or goal_positions:
        ax.legend(loc="upper right", fontsize="small")

    ax.set_xticks(np.arange(0, width))
    ax.set_yticks(np.arange(0, height))
    ax.set_xticklabels([str(i) for i in range(0, width)])

    ax.set_yticklabels([str(i) for i in range(height - 1, -1, -1)])
    ax.set_xlim(-0.5, width - 0.5)
    ax.set_ylim(-0.5, height - 0.5)
    ax.invert_yaxis()

    save_or_show(fig, outdir, "heatmap")


def plot_paths(best_paths: List[List[tuple]], avg_fitness: List[float], env, outdir: Optional[Path], start_positions=None, goal_positions=None):
    width, height = env.width, env.height
    n = len(best_paths)
    if n == 0:
        print("No best paths to plot")
        return

    fig, ax = plt.subplots(figsize=(7, 7))

    # Draw map items (walls, eggs, nests, stones, coop) behind the paths
    from Items.Wall import Wall
    from Items.Egg import Egg
    from Items.Nest import Nest
    from Items.Stone import Stone
    from Items.ChickenCoop import ChickenCoop

    for y in range(height):
        for x in range(width):
            tile = env.map[y][x]
            if tile is None:
                continue
            if isinstance(tile, Wall):
                rect = Rectangle((x - 0.5, y - 0.5), 1, 1, facecolor="#888888", edgecolor="#444444", linewidth=0.5, zorder=0)
                ax.add_patch(rect)
            elif isinstance(tile, Egg):
                ax.text(x + 0.0, y + 0.0, "E", color="black", fontsize=8, weight="bold", ha="center", va="center", zorder=2)
            elif isinstance(tile, Nest):
                ax.text(x + 0.0, y + 0.0, "N", color="purple", fontsize=8, weight="bold", ha="center", va="center", zorder=2)
            elif isinstance(tile, Stone):
                ax.text(x + 0.0, y + 0.0, "S", color="saddlebrown", fontsize=8, weight="bold", ha="center", va="center", zorder=2)
            elif isinstance(tile, ChickenCoop):
                ax.text(x + 0.0, y + 0.0, "F", color="blue", fontsize=10, weight="bold", ha="center", va="center", zorder=2)

    max_lines = min(n, 3)
    if n <= max_lines:
        indices = list(range(n))
    else:
        indices = sorted({int(round(i * (n - 1) / (max_lines - 1))) for i in range(max_lines)})

    cmap = plt.get_cmap('tab20')
    colors = [cmap(i / max(1, len(indices) - 1)) for i in range(len(indices))]

    for draw_idx, gen_idx in enumerate(indices):
        path = best_paths[gen_idx]
        if not path:
            continue
        xs = [p[0] for p in path]
        ys = [p[1] for p in path]

        t = draw_idx / max(1, len(indices) - 1)
        linewidth = 1.0 + 2.0 * t
        alpha = 0.35 + 0.65 * t
        color = colors[draw_idx % len(colors)]

        pe = [path_effects.Stroke(linewidth=linewidth + 1.2, foreground='black'), path_effects.Normal()]
        line, = ax.plot(xs, ys, lw=linewidth, color=color, alpha=alpha, label=f"Gen {gen_idx+1}", zorder=3 + draw_idx)
        try:
            line.set_path_effects(pe)
        except Exception:
            pass

        # Start marker (small filled circle) and end marker (larger X)
        if xs and ys:
            ax.scatter(xs[0], ys[0], marker='o', color=color, edgecolor='k', s=50, zorder=4 + draw_idx)
            ax.scatter(xs[-1], ys[-1], marker='X', color=color, edgecolor='k', s=70, zorder=4 + draw_idx)

    # Provide a legend that doesn't overcrowd the figure: show only the sampled gens
    if len(indices) > 0:
        ax.legend(loc='best', fontsize='small')

    ax.set_xlim(-0.5, width - 0.5)
    ax.set_ylim(-0.5, height - 0.5)
    ax.set_aspect("equal")
    ax.invert_yaxis()
    ax.set_title("Best Paths — sample generations")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend(loc="best", fontsize="small")
    ax.grid(alpha=0.25)

    # plot starts (distinct marker)
    if start_positions:
        sx = [p[0] for p in start_positions]
        sy = [p[1] for p in start_positions]
        ax.scatter(sx, sy, marker="^", color="green", s=120, edgecolor="k", label="start(s)", zorder=6)

    # plot goals
    if goal_positions:
        if isinstance(goal_positions, tuple):
            goal_positions = [goal_positions]
        gx = [p[0] for p in goal_positions]
        gy = [p[1] for p in goal_positions]
        ax.scatter(gx, gy, marker="s", color="red", s=140, edgecolor="k", label="goal(s)", zorder=6)

    if start_positions or goal_positions:
        ax.legend(loc="best", fontsize="small")

    ax.set_xticks(np.arange(0, width))
    ax.set_yticks(np.arange(0, height))
    ax.set_xticklabels([str(i) for i in range(0, width)])

    ax.set_yticklabels([str(i) for i in range(height - 1, -1, -1)])

    save_or_show(fig, outdir, "paths")


def plot_avg_fitness(avg_fitness: List[float], outdir: Optional[Path]):
    fig, ax = plt.subplots(figsize=(6, 3.5))
    gens = np.arange(1, len(avg_fitness) + 1)
    ax.plot(gens, avg_fitness, marker="o", lw=2, color="#2b8cbe")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Average combined fitness")
    ax.set_title("Average Combined Fitness per Generation")
    ax.grid(alpha=0.3)
    save_or_show(fig, outdir, "avg_fitness")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--map", "-m", default="Levels/simple_foraging.txt", help="Level/map file")
    p.add_argument("--pop", "-p", type=int, default=40, help="Population size")
    p.add_argument("--gens", "-g", type=int, default=20, help="Number of generations")
    p.add_argument("--outdir", "-o", default=None, help="Directory to save plots (if omitted, show interactively)")
    p.add_argument("--headless", action="store_true", help="Run evolution headless (no visual episode playback)")
    args = p.parse_args()

    outdir = Path(args.outdir) if args.outdir else None
    if outdir:
        outdir.mkdir(parents=True, exist_ok=True)

    # Create motor first so we can capture initial agent start positions
    motor = SimulatorMotor.create(args.map, headless=args.headless, single_run=False)
    motor.POPULATION_SIZE = args.pop
    motor.NUM_GENERATIONS = args.gens

    # capture initial starts (read from map file so they reflect the map)
    env = motor.world
    starts = parse_start_positions(motor.map_file_path if hasattr(motor, 'map_file_path') else args.map)
    goals = None
    if isinstance(env, CoopWorld):
        goals = env.chicken_coop.position if env.chicken_coop else None
    else:
        goals = [n.position for n in getattr(env, "nests", [])]

    # Run the evolution (this will populate history fields)
    motor.execute()

    # Collected history
    best_paths = getattr(motor, "best_paths_per_gen", [])
    avg_fitness = getattr(motor, "avg_fitness_per_gen", [])
    best_behaviors = getattr(motor, "best_behaviors", [])


    # Produce plots (pass starts/goals captured before execution)
    plot_heatmap(best_behaviors, env, generations=len(best_paths), outdir=outdir, start_positions=starts, goal_positions=goals)
    plot_paths(best_paths, avg_fitness, env, outdir=outdir, start_positions=starts, goal_positions=goals)
    plot_avg_fitness(avg_fitness, outdir=outdir)


if __name__ == "__main__":
    main()

# example run : 
# python3 -m visualization.visualize --map Levels/farol_level2.txt --pop 40 --gens 40 --outdir results

def visualize_graphs(motor, outdir: Optional[Path] = "results"):
    """Visualize graphs from a SimulatorMotor instance.

    outdir may be a string or a Path; if provided it will be created.
    This function also computes and passes start/goal positions so markers
    appear on both the heatmap and path plots.
    """
    # normalize outdir to Path | None
    if outdir:
        outdir = Path(outdir)
        outdir.mkdir(parents=True, exist_ok=True)

    env = motor.world

    # Collected history
    best_paths = getattr(motor, "best_paths_per_gen", [])
    avg_fitness = getattr(motor, "avg_fitness_per_gen", [])
    best_behaviors = getattr(motor, "best_behaviors", [])

    # compute starts/goals: prefer positions parsed from the original map file
    starts = parse_start_positions(motor.map_file_path if hasattr(motor, 'map_file_path') else None)
    goals = None
    if isinstance(env, CoopWorld):
        goals = env.chicken_coop.position if env.chicken_coop else None
    else:
        goals = [n.position for n in getattr(env, "nests", [])]

    # Produce plots (pass starts/goals)
    plot_heatmap(best_behaviors, env, generations=len(best_paths), outdir=outdir, start_positions=starts, goal_positions=goals)
    plot_paths(best_paths, avg_fitness, env, outdir=outdir, start_positions=starts, goal_positions=goals)
    plot_avg_fitness(avg_fitness, outdir=outdir)