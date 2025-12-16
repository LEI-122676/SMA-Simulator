#!/usr/bin/env python3
"""
Simple visualization runner for SMA-Simulator.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from typing import List, Optional, Dict, Tuple

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns
from matplotlib import patheffects as path_effects

from Simulators.SimulatorMotor import SimulatorMotor
from Worlds.CoopWorld import CoopWorld

# Configuration for map elements: (Color, Label)
ITEM_STYLE = {
    'Wall': ('#888888', ''), 'Egg': ('black', 'E'), 
    'Nest': ('purple', 'N'), 'Stone': ('saddlebrown', 'S'),
    'ChickenCoop': ('blue', 'F')
}

def parse_map_layout(map_path: Optional[str]) -> Dict[str, List[Tuple[int, int]]]:
    """Parses map file once and groups coordinates by item type."""
    data = {k: [] for k in ['Wall', 'Egg', 'Nest', 'Stone', 'ChickenCoop', 'Start']}
    char_map = {'W': 'Wall', 'E': 'Egg', 'N': 'Nest', 'S': 'Stone', 'F': 'ChickenCoop', 'C': 'Start'}
    
    if not map_path: return data
    
    try:
        with open(map_path, 'r') as f:
            for y, line in enumerate(f.readlines()):
                for x, ch in enumerate(line.rstrip('\n')):
                    if ch in char_map:
                        data[char_map[ch]].append((x, y))
    except Exception:
        pass
    return data

def _save_plot(fig, outdir: Optional[Path], name: str):
    if outdir:
        path = outdir / f"{name}.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"Saved {path}")
    else:
        fig.show()

def _draw_map_elements(ax, items: Dict, width: int, height: int):
    """Helper to draw static map items (Walls, etc) on any plot."""
    # Draw Grid/Board boundaries
    ax.set_xlim(-0.5, width - 0.5)
    ax.set_ylim(-0.5, height - 0.5)
    ax.set_xticks(np.arange(0, width))
    ax.set_yticks(np.arange(0, height))
    ax.invert_yaxis()
    ax.set_aspect("equal")

    # Draw Items
    for item_type, positions in items.items():
        if item_type not in ITEM_STYLE: continue
        color, label = ITEM_STYLE[item_type]
        
        for (x, y) in positions:
            if item_type == 'Wall':
                ax.add_patch(Rectangle((x - 0.5, y - 0.5), 1, 1, facecolor=color, edgecolor="#444444", lw=0.5))
            else:
                txt = ax.text(x, y, label, color=color, fontsize=9, weight="bold", ha="center", va="center")
                txt.set_path_effects([path_effects.Stroke(linewidth=1.5, foreground='white'), path_effects.Normal()])

def plot_heatmap(behaviors, env, items, outdir):
    h, w = env.height, env.width
    grid = np.zeros((h, w))
    
    for beh in behaviors:
        for x, y in beh:
            if 0 <= x < w and 0 <= y < h:
                grid[int(y), int(x)] += 1

    fig, ax = plt.subplots(figsize=(6, 6))
    sns.heatmap(grid, ax=ax, cmap="YlOrRd", cbar_kws={"label": "visits"}, zorder=0)
    
    _draw_map_elements(ax, items, w, h)
    ax.set_title(f"Visited Areas Heatmap")
    _save_plot(fig, outdir, "heatmap")

def plot_paths(paths, env, items, outdir):
    if not paths: return
    fig, ax = plt.subplots(figsize=(7, 7))
    _draw_map_elements(ax, items, env.width, env.height)

    # Select up to 3 representative paths
    indices = np.linspace(0, len(paths)-1, min(len(paths), 3), dtype=int)
    cmap = plt.get_cmap('tab20')
    
    for i, idx in enumerate(indices):
        path = paths[idx]
        if not path: continue
        xs, ys = zip(*path)
        
        color = cmap(i / len(indices))
        ax.plot(xs, ys, lw=2 + i, color=color, alpha=0.8, label=f"Gen {idx+1}", 
                path_effects=[path_effects.Stroke(linewidth=4, foreground='black'), path_effects.Normal()])
        
        # Start/End markers
        ax.scatter(xs[0], ys[0], c=[color], marker='o', s=50, edgecolors='k', zorder=10)
        ax.scatter(xs[-1], ys[-1], c=[color], marker='X', s=80, edgecolors='k', zorder=10)

    ax.legend(loc='best', fontsize='small')
    ax.set_title("Best Paths (Sampled)")
    _save_plot(fig, outdir, "paths")

def plot_fitness(fitness_hist, outdir):
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.plot(range(1, len(fitness_hist) + 1), fitness_hist, marker="o", lw=2, color="#2b8cbe")
    ax.set_title("Average Combined Fitness")
    ax.set_xlabel("Generation")
    ax.grid(alpha=0.3)
    _save_plot(fig, outdir, "avg_fitness")

def visualize_graphs(motor, outdir: Optional[str] = "results"):
    """Main visualization driver."""
    out_path = Path(outdir) if outdir else None
    if out_path: out_path.mkdir(parents=True, exist_ok=True)

    env = motor.world
    map_file = getattr(motor, 'map_file_path', None)
    
    # Parse static map items
    items = parse_map_layout(map_file)
    
    # Add Goals manually to the items dict for drawing
    goals = []
    if isinstance(env, CoopWorld) and env.chicken_coop:
        goals = [env.chicken_coop.position]
    elif hasattr(env, "nests"):
        goals = [n.position for n in env.nests]
    
    # Plotting
    plot_heatmap(getattr(motor, "best_behaviors", []), env, items, out_path)
    plot_paths(getattr(motor, "best_paths_per_gen", []), env, items, out_path)
    plot_fitness(getattr(motor, "avg_fitness_per_gen", []), out_path)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--map", "-m", default="Levels/simple_foraging.txt")
    p.add_argument("--pop", "-p", type=int, default=40)
    p.add_argument("--gens", "-g", type=int, default=20)
    p.add_argument("--outdir", "-o", default=None)
    p.add_argument("--headless", action="store_true")
    args = p.parse_args()

    # Init and Run
    motor = SimulatorMotor.create(args.map, headless=args.headless, single_run=False)
    motor.POPULATION_SIZE = args.pop
    motor.NUM_GENERATIONS = args.gens
    motor.execute()

    # Visualize
    visualize_graphs(motor, args.outdir)

if __name__ == "__main__":
    main()