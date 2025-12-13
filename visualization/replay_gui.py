"""Replay GUI for best agent per generation

Usage:
  python3 visualization/replay_gui.py

Features:
- Load a map file (Levels/*.txt) to draw walls/items
- Load an evolution state pickle (default: evolution_state.pkl)
- Pick a generation and replay the recorded best path step-by-step

This lightweight GUI uses tkinter + matplotlib and depends only on stdlib + matplotlib.

Quick start:
# run a short evolution (saves evolution_state.pkl)
python3 -m visualization.visualize --map Levels/foraging_level2.txt --pop 8 --gens 3 --outdir results_test --headless

# open the GUI (needs a display / X forwarding)
python3 visualization/replay_gui.py
"""
from __future__ import annotations
import pickle
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from typing import List, Tuple, Optional

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def parse_map_file(map_path: Path) -> Tuple[List[str], int, int]:
    with open(map_path, "r") as f:
        lines = [ln.rstrip("\n") for ln in f.readlines() if ln.strip() != ""]
    height = len(lines)
    width = max(len(ln) for ln in lines) if lines else 0
    # Normalize line lengths
    lines = [ln.ljust(width, '.') for ln in lines]
    return lines, width, height


def parse_state_file(state_path: Path) -> dict:
    with open(state_path, "rb") as f:
        return pickle.load(f)


class ReplayGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Evolution Replay — Best Agent per Generation")

        # State
        self.map_lines: List[str] = []
        self.map_w = 0
        self.map_h = 0
        self.state = None
        self.best_paths: List[List[Tuple[int, int]]] = []
        self.generation = 0
        self.frame_index = 0
        self.playing = False
        self.after_id = None

        self._build_ui()

    def _build_ui(self):
        frm = tk.Frame(self.root)
        frm.pack(side=tk.TOP, fill=tk.X, padx=6, pady=6)

        tk.Label(frm, text="Map file:").grid(row=0, column=0, sticky=tk.W)
        self.map_entry = tk.Entry(frm, width=40)
        self.map_entry.grid(row=0, column=1, padx=4)
        tk.Button(frm, text="Browse", command=self.browse_map).grid(row=0, column=2, padx=4)

        tk.Label(frm, text="State (pickle):").grid(row=1, column=0, sticky=tk.W)
        self.state_entry = tk.Entry(frm, width=40)
        self.state_entry.grid(row=1, column=1, padx=4)
        tk.Button(frm, text="Browse", command=self.browse_state).grid(row=1, column=2, padx=4)

        tk.Button(frm, text="Load", command=self.load_all).grid(row=2, column=0, columnspan=3, pady=6)

        # Controls
        ctl = tk.Frame(self.root)
        ctl.pack(side=tk.TOP, fill=tk.X, padx=6)

        tk.Label(ctl, text="Generation:").pack(side=tk.LEFT)
        self.gen_slider = tk.Scale(ctl, from_=0, to=0, orient=tk.HORIZONTAL, length=300, command=self.on_gen_change)
        self.gen_slider.pack(side=tk.LEFT, padx=8)

        self.play_button = tk.Button(ctl, text="Play", command=self.toggle_play)
        self.play_button.pack(side=tk.LEFT, padx=6)
        tk.Button(ctl, text="Step >>", command=self.step_forward).pack(side=tk.LEFT, padx=2)
        tk.Button(ctl, text="<< Step", command=self.step_backward).pack(side=tk.LEFT, padx=2)

        # Canvas
        self.fig = Figure(figsize=(6, 6))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Frame slider
        frame_fr = tk.Frame(self.root)
        frame_fr.pack(side=tk.TOP, fill=tk.X, padx=6, pady=4)
        tk.Label(frame_fr, text="Frame:").pack(side=tk.LEFT)
        self.frame_slider = tk.Scale(frame_fr, from_=0, to=0, orient=tk.HORIZONTAL, length=400, command=self.on_frame_change)
        self.frame_slider.pack(side=tk.LEFT, padx=6)

    def browse_map(self):
        p = filedialog.askopenfilename(title="Select map file", filetypes=[("Text files","*.txt"), ("All files","*")])
        if p:
            self.map_entry.delete(0, tk.END)
            self.map_entry.insert(0, p)

    def browse_state(self):
        p = filedialog.askopenfilename(title="Select state pickle", filetypes=[("Pickle files","*.pkl;*.pickle"), ("All files","*")])
        if p:
            self.state_entry.delete(0, tk.END)
            self.state_entry.insert(0, p)

    def load_all(self):
        map_path = self.map_entry.get().strip()
        state_path = self.state_entry.get().strip() or "evolution_state.pkl"

        # If user didn't set a map but the state file contains it, use it
        try:
            self.state = parse_state_file(Path(state_path))
        except Exception as e:
            messagebox.showerror("Error", f"Failed reading state pickle: {e}")
            return

        # Prefer map path from map_entry but fall back to various keys in the state
        if not map_path:
            map_from_state = None
            if isinstance(self.state, dict):
                # common candidate keys
                for k in ("map", "map_path", "mapfile", "map_file_path", "mapFile", "mapPath"):
                    if k in self.state and self.state[k]:
                        map_from_state = self.state[k]
                        break

            # If found in state, resolve relative paths against the state file location
            if map_from_state:
                try:
                    sp = Path(state_path)
                    candidate = Path(map_from_state)
                    if not candidate.is_absolute() and sp.exists():
                        candidate = (sp.parent / candidate).resolve()
                    map_path = str(candidate)
                except Exception:
                    map_path = str(map_from_state)

            # If still not found, try to auto-discover map files nearby
            if not map_path:
                candidates = []
                sp = Path(state_path)
                # search in same dir as state
                if sp.exists():
                    candidates.extend(list(sp.parent.glob("*.txt")))
                # search in Levels/
                levels_dir = Path("Levels")
                if levels_dir.exists():
                    candidates.extend(list(levels_dir.glob("*.txt")))
                # dedupe
                candidates = [p for i, p in enumerate(candidates) if p not in candidates[:i]]

                # Try to pick the best candidate based on recorded paths in the state.
                # We prefer map files whose dimensions contain the path coordinates
                # and whose 'C' start positions match path starts when possible.
                selected = None
                try:
                    # gather recorded coordinate bounds from state
                    coords = []
                    # prefer explicit 'paths' (current run) then fall back to best_paths_per_gen
                    if isinstance(self.state, dict):
                        if isinstance(self.state.get('paths'), list) and any(self.state.get('paths')):
                            for p in self.state.get('paths'):
                                if isinstance(p, list):
                                    coords.extend([tuple(pt) for pt in p if isinstance(pt, (list, tuple)) and len(pt) >= 2])
                        if not coords and isinstance(self.state.get('best_paths_per_gen'), list):
                            for p in self.state.get('best_paths_per_gen'):
                                if isinstance(p, list):
                                    coords.extend([tuple(pt) for pt in p if isinstance(pt, (list, tuple)) and len(pt) >= 2])
                    max_x = max((c[0] for c in coords), default=None)
                    max_y = max((c[1] for c in coords), default=None)

                    # prefer candidates that can contain the recorded coords
                    good = []
                    for cand in candidates:
                        try:
                            lines, w, h = parse_map_file(cand)
                        except Exception:
                            continue
                        fits = True
                        if max_x is not None and max_y is not None:
                            if max_x >= w or max_y >= h:
                                fits = False
                        if fits:
                            good.append((cand, lines, w, h))

                    # If we have filtered set, prefer ones with matching 'C' start positions
                    if good:
                        # find recorded path starts
                        path_starts = set()
                        for p in coords:
                            path_starts.add((p[0], p[1]))

                        scored = []
                        for cand, lines, w, h in good:
                            # parse C positions
                            c_positions = set()
                            for y, ln in enumerate(lines):
                                for x, ch in enumerate(ln):
                                    if ch == 'C':
                                        c_positions.add((x, y))
                            # score by intersection size with path starts
                            score = len(path_starts & c_positions) if path_starts else 0
                            scored.append((score, cand))

                        # pick highest score, then first
                        scored.sort(key=lambda x: (-x[0], str(x[1])))
                        selected = scored[0][1] if scored else good[0][0]
                    elif candidates:
                        # fallback: pick the first candidate
                        selected = candidates[0]
                except Exception:
                    selected = candidates[0] if candidates else None

                if selected:
                    map_path = str(Path(selected).resolve())
                    if len(candidates) > 1:
                        messagebox.showinfo("Auto-selected map", f"Multiple map candidates found; using: {map_path}")
                    else:
                        messagebox.showinfo("Auto-selected map", f"Auto-selected map file: {map_path}")

        if not map_path:
            messagebox.showerror("Error", "Please select a map file (or include map path in the state pickle).")
            return

        try:
            self.map_lines, self.map_w, self.map_h = parse_map_file(Path(map_path))
        except Exception as e:
            messagebox.showerror("Error", f"Failed reading map file: {e}")
            return

        self.best_paths = self.state.get("best_paths_per_gen", []) or []
        if not self.best_paths:
            messagebox.showinfo("No data", "No best_paths_per_gen found in the state file.")

        # configure sliders
        self.gen_slider.config(to=max(0, len(self.best_paths)-1))
        self.gen_slider.set(0)
        self.on_gen_change(0)

        self.redraw()

    def on_gen_change(self, val):
        try:
            self.generation = int(val)
        except Exception:
            self.generation = 0
        # rebuild frame slider depending on path length
        path = self.best_paths[self.generation] if self.best_paths and self.generation < len(self.best_paths) else []
        maxf = max(0, len(path)-1)
        self.frame_slider.config(to=maxf)
        self.frame_slider.set(0)
        self.frame_index = 0
        self.redraw()

    def on_frame_change(self, val):
        try:
            self.frame_index = int(val)
        except Exception:
            self.frame_index = 0
        self.redraw()

    def toggle_play(self):
        if self.playing:
            self.playing = False
            self.play_button.config(text="Play")
            if self.after_id:
                self.root.after_cancel(self.after_id)
                self.after_id = None
        else:
            self.playing = True
            self.play_button.config(text="Pause")
            self._play_loop()

    def _play_loop(self):
        path = self.best_paths[self.generation] if self.best_paths and self.generation < len(self.best_paths) else []
        if not path:
            self.playing = False
            self.play_button.config(text="Play")
            return
        # advance frame
        self.frame_index = (self.frame_index + 1) % max(1, len(path))
        self.frame_slider.set(self.frame_index)
        self.redraw()
        if self.playing:
            self.after_id = self.root.after(300, self._play_loop)

    def step_forward(self):
        self.frame_index = min(self.frame_slider['to'], self.frame_index + 1)
        self.frame_slider.set(self.frame_index)
        self.redraw()

    def step_backward(self):
        self.frame_index = max(0, self.frame_index - 1)
        self.frame_slider.set(self.frame_index)
        self.redraw()

    def redraw(self):
        self.ax.clear()
        # Draw grid background
        if self.map_lines:
            grid = [[1 if ch == 'W' else 0 for ch in line] for line in self.map_lines]
            import numpy as _np
            mat = _np.array(grid)
            # draw walls as dark squares
            self.ax.imshow(mat, cmap='Greys', origin='upper', interpolation='nearest')
            # Draw other items as text
            for y, line in enumerate(self.map_lines):
                for x, ch in enumerate(line):
                    if ch == 'E':
                        self.ax.text(x, y, 'E', color='gold', fontsize=10, ha='center', va='center')
                    elif ch == 'N':
                        self.ax.text(x, y, 'N', color='purple', fontsize=10, ha='center', va='center')
                    elif ch == 'F':
                        self.ax.text(x, y, 'F', color='blue', fontsize=10, ha='center', va='center')
                    elif ch == 'S':
                        self.ax.text(x, y, 'S', color='saddlebrown', fontsize=10, ha='center', va='center')
                    elif ch == 'C':
                        self.ax.text(x, y, 'C', color='green', fontsize=10, ha='center', va='center')
        else:
            self.ax.set_xlim(-0.5, 9.5)
            self.ax.set_ylim(-0.5, 9.5)

        # Draw selected generation best path
        path = self.best_paths[self.generation] if self.best_paths and self.generation < len(self.best_paths) else []
        xs = [p[0] for p in path]
        ys = [p[1] for p in path]
        if xs and ys:
            self.ax.plot(xs, ys, color='cyan', linewidth=2, marker='o')
            # draw moving agent marker
            if 0 <= self.frame_index < len(xs):
                self.ax.scatter([xs[self.frame_index]], [ys[self.frame_index]], color='red', s=80, zorder=5)

        self.ax.set_aspect('equal')
        self.ax.invert_yaxis()
        # ticks
        if self.map_w:
            self.ax.set_xticks(range(self.map_w))
            self.ax.set_yticks(range(self.map_h))
        self.canvas.draw()


if __name__ == '__main__':
    root = tk.Tk()
    app = ReplayGUI(root)

    # Auto-attempt to load a default state file if present so the user
    # doesn't have to press Load manually. This helps when the pickle
    # was just produced in the same working directory (common usage).
    default_state = Path("evolution_state.pkl")
    try:
        if default_state.exists():
            app.state_entry.delete(0, tk.END)
            app.state_entry.insert(0, str(default_state))
            # call load_all to populate map/state; swallow exceptions
            try:
                app.load_all()
            except Exception:
                pass
    except Exception:
        pass

    root.mainloop()
