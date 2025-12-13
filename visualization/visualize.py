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
import seaborn as sns

from Simulators.SimulatorMotor import SimulatorMotor
from Worlds.CoopWorld import CoopWorld


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
    sns.heatmap(heatmap, ax=ax, cmap="YlOrRd", cbar_kws={"label": "visits"})
    ax.invert_yaxis()
    ax.set_title(f"Visited Areas Heatmap — {generations} gens")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    # Add world labels (eggs/nests/coop) if available
    if hasattr(env, "eggs"):
        for egg in getattr(env, "eggs", []):
            x, y = egg.position
            ax.text(x + 0.3, y + 0.3, "E", color="black", fontsize=8, weight="bold", ha="center", va="center")
    if hasattr(env, "nests"):
        for nest in getattr(env, "nests", []):
            x, y = nest.position
            ax.text(x + 0.3, y + 0.3, "N", color="purple", fontsize=8, weight="bold", ha="center", va="center")
    coop = getattr(env, "chicken_coop", None)
    if coop is not None:
        x, y = coop.position
        ax.text(x + 0.3, y + 0.3, "F", color="blue", fontsize=10, weight="bold", ha="center", va="center")

    # Plot start positions
    if start_positions:
        sx = [p[0] for p in start_positions]
        sy = [p[1] for p in start_positions]
        ax.scatter(sx, sy, marker="^", color="green", s=80, edgecolor="k", label="start(s)")

    # Plot goal positions
    if goal_positions:
        if isinstance(goal_positions, tuple):
            goal_positions = [goal_positions]
        gx = [p[0] for p in goal_positions]
        gy = [p[1] for p in goal_positions]
        ax.scatter(gx, gy, marker="s", color="red", s=100, edgecolor="k", label="goal(s)")

    if start_positions or goal_positions:
        ax.legend(loc="upper right", fontsize="small")

    save_or_show(fig, outdir, "heatmap")


def plot_paths(best_paths: List[List[tuple]], avg_fitness: List[float], env, outdir: Optional[Path], start_positions=None, goal_positions=None):
    width, height = env.width, env.height
    n = len(best_paths)
    if n == 0:
        print("No best paths to plot")
        return

    fig, ax = plt.subplots(figsize=(7, 7))
    colors = cm.viridis(np.linspace(0, 1, min(8, n)))

    # pick up to 4 generations evenly spaced
    indices = [0]
    if n > 1:
        indices = [0, n // 3, 2 * n // 3, n - 1]
        indices = sorted(set(i for i in indices if i < n))

    for idx, i in enumerate(indices):
        path = best_paths[i]
        if not path:
            continue
        xs = [p[0] for p in path]
        ys = [p[1] for p in path]
        color = colors[idx % len(colors)]
        avg_label = ""
        if i < len(avg_fitness):
            avg_label = f" (avg {avg_fitness[i]:.1f})"
        ax.plot(xs, ys, lw=2.2, color=color, alpha=0.9, label=f"Gen {i+1}{avg_label}")
        ax.scatter(xs[0], ys[0], marker="o", color=color, edgecolor="k", s=80)
        ax.scatter(xs[-1], ys[-1], marker="X", color=color, edgecolor="k", s=100)

    # plot starts (distinct marker)
    if start_positions:
        sx = [p[0] for p in start_positions]
        sy = [p[1] for p in start_positions]
        ax.scatter(sx, sy, marker="^", color="green", s=90, edgecolor="k", label="start(s)")

    # plot goals
    if goal_positions:
        if isinstance(goal_positions, tuple):
            goal_positions = [goal_positions]
        gx = [p[0] for p in goal_positions]
        gy = [p[1] for p in goal_positions]
        ax.scatter(gx, gy, marker="s", color="red", s=110, edgecolor="k", label="goal(s)")

    ax.set_xlim(-0.5, width - 0.5)
    ax.set_ylim(-0.5, height - 0.5)
    ax.set_aspect("equal")
    ax.invert_yaxis()
    ax.set_title("Best Paths — sample generations")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend(loc="best", fontsize="small")
    ax.grid(alpha=0.25)

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

    # capture initial starts (before any simulation moves agents)
    env = motor.world
    starts = [agent.position for agent in env.agents]
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

    # compute starts/goals from the environment so they are shown on plots
    starts = [agent.position for agent in env.agents]
    goals = None
    if isinstance(env, CoopWorld):
        goals = env.chicken_coop.position if env.chicken_coop else None
    else:
        goals = [n.position for n in getattr(env, "nests", [])]

    # Produce plots (pass starts/goals)
    plot_heatmap(best_behaviors, env, generations=len(best_paths), outdir=outdir, start_positions=starts, goal_positions=goals)
    plot_paths(best_paths, avg_fitness, env, outdir=outdir, start_positions=starts, goal_positions=goals)
    plot_avg_fitness(avg_fitness, outdir=outdir)