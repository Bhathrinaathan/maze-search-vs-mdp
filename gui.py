import tkinter as tk
from tkinter import ttk
import csv
import os
from datetime import datetime

from maze import Maze
import bfs
import dfs
import astar_manhattan
import astar_euclidean
import value_iteration
import policy_iteration

ALGORITHMS = {
    'BFS': bfs,
    'DFS': dfs,
    'A* Manhattan': astar_manhattan,
    'A* Euclidean': astar_euclidean,
    'Value Iteration': value_iteration,
    'Policy Iteration': policy_iteration,
}

ALGO_COLORS = {
    'BFS': '#3498db',
    'DFS': '#e67e22',
    'A* Manhattan': '#2ecc71',
    'A* Euclidean': '#9b59b6',
    'Value Iteration': '#1abc9c',
    'Policy Iteration': '#f39c12',
}

WALL_COLOR = '#2c3e50'
PATH_COLOR = 'white'
START_COLOR = '#27ae60'
GOAL_COLOR = '#e74c3c'
VISITED_COLOR = '#85c1e9'
SOLUTION_COLOR = '#f1c40f'


class MazeSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver - CS7IS2 AI Assignment 1")
        self.root.geometry("1050x750")
        self.root.minsize(850, 650)

        self.maze = None
        self.cell_size = 20
        self.cells = {}
        self.animating = False
        self._animation_id = None

        self._build_ui()

    def _build_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Left panel ---
        left_frame = tk.Frame(main_frame, width=280, padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        left_frame.pack_propagate(False)

        tk.Label(left_frame, text="Maze Solver",
                 font=("Helvetica", 16, "bold")).pack(pady=(0, 8))

        # Maze generation
        gen_frame = tk.LabelFrame(left_frame, text="Generate", padx=5, pady=5)
        gen_frame.pack(fill=tk.X, pady=3)

        size_frame = tk.Frame(gen_frame)
        size_frame.pack(fill=tk.X)
        tk.Label(size_frame, text="Rows:").pack(side=tk.LEFT)
        self.rows_var = tk.IntVar(value=10)
        tk.Spinbox(size_frame, from_=5, to=25,
                   textvariable=self.rows_var, width=4).pack(side=tk.LEFT, padx=2)
        tk.Label(size_frame, text="Cols:").pack(side=tk.LEFT, padx=(8, 0))
        self.cols_var = tk.IntVar(value=10)
        tk.Spinbox(size_frame, from_=5, to=25,
                   textvariable=self.cols_var, width=4).pack(side=tk.LEFT, padx=2)

        tk.Button(gen_frame, text="Generate Maze",
                  command=self.generate_maze).pack(fill=tk.X, pady=(5, 0))

        # Algorithm selection
        algo_frame = tk.LabelFrame(left_frame, text="Algorithm", padx=5, pady=3)
        algo_frame.pack(fill=tk.X, pady=3)

        self.algo_var = tk.StringVar(value="BFS")
        for algo in ALGORITHMS:
            tk.Radiobutton(algo_frame, text=algo,
                           variable=self.algo_var, value=algo).pack(anchor=tk.W)

        # Solve controls
        solve_frame = tk.LabelFrame(left_frame, text="Solve", padx=5, pady=5)
        solve_frame.pack(fill=tk.X, pady=3)

        tk.Button(solve_frame, text="Solve",
                  command=self.solve).pack(fill=tk.X, pady=1)
        tk.Button(solve_frame, text="Solve All (6 algorithms)",
                  command=self.solve_all).pack(fill=tk.X, pady=1)

        btn_row = tk.Frame(solve_frame)
        btn_row.pack(fill=tk.X, pady=2)
        tk.Button(btn_row, text="Clear Solution",
                  command=self.clear_solution).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        tk.Button(btn_row, text="Reset",
                  command=self.reset).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))

        # Statistics
        stats_frame = tk.LabelFrame(left_frame, text="Statistics", padx=5, pady=5)
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=3)

        self.stats_text = tk.Text(stats_frame, height=8, width=30,
                                  state=tk.DISABLED, font=("Courier", 9))
        stats_scroll = tk.Scrollbar(stats_frame, command=self.stats_text.yview)
        self.stats_text.config(yscrollcommand=stats_scroll.set)
        stats_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.stats_text.pack(fill=tk.BOTH, expand=True)

        # Legend
        legend_frame = tk.LabelFrame(left_frame, text="Legend", padx=5, pady=3)
        legend_frame.pack(fill=tk.X, pady=3)

        legend_items = [
            ("Start", START_COLOR), ("Goal", GOAL_COLOR),
            ("Visited", VISITED_COLOR), ("Path", SOLUTION_COLOR),
        ]
        legend_grid = tk.Frame(legend_frame)
        legend_grid.pack(fill=tk.X)
        for i, (name, color) in enumerate(legend_items):
            row_i = i // 2
            col_i = i % 2
            f = tk.Frame(legend_grid)
            f.grid(row=row_i, column=col_i, sticky=tk.W, padx=2, pady=1)
            c = tk.Canvas(f, width=12, height=12, highlightthickness=0)
            c.create_rectangle(0, 0, 12, 12, fill=color, outline='')
            c.pack(side=tk.LEFT, padx=(0, 3))
            tk.Label(f, text=name, font=("Helvetica", 9)).pack(side=tk.LEFT)

        # Algorithm color legend
        ttk.Separator(legend_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=2)
        algo_legend_grid = tk.Frame(legend_frame)
        algo_legend_grid.pack(fill=tk.X)
        for i, (aname, acolor) in enumerate(ALGO_COLORS.items()):
            row_i = i // 2
            col_i = i % 2
            f = tk.Frame(algo_legend_grid)
            f.grid(row=row_i, column=col_i, sticky=tk.W, padx=2, pady=0)
            c = tk.Canvas(f, width=10, height=10, highlightthickness=0)
            c.create_rectangle(0, 0, 10, 10, fill=acolor, outline='')
            c.pack(side=tk.LEFT, padx=(0, 2))
            short = aname.replace("Iteration", "Iter.")
            tk.Label(f, text=short, font=("Helvetica", 8)).pack(side=tk.LEFT)

        # --- Right panel (canvas) ---
        canvas_frame = tk.Frame(main_frame, bg='#bdc3c7')
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg='#ecf0f1', highlightthickness=0)
        self.canvas.pack(padx=20, pady=20)

    # ── Maze generation ──────────────────────────────────────────

    def generate_maze(self):
        if self.animating:
            return
        rows = self.rows_var.get()
        cols = self.cols_var.get()
        self.maze = Maze(rows, cols)
        self.maze.generate()
        self.draw_maze()
        self.update_stats("")

    # ── Drawing ──────────────────────────────────────────────────

    def draw_maze(self):
        if not self.maze:
            return
        self.cell_size = max(4, min(25, 600 // max(self.maze.height, self.maze.width)))
        canvas_w = self.maze.width * self.cell_size
        canvas_h = self.maze.height * self.cell_size
        self.canvas.config(width=canvas_w, height=canvas_h)
        self.canvas.delete("all")
        self.cells = {}

        for r in range(self.maze.height):
            for c in range(self.maze.width):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                if self.maze.grid[r][c] == 1:
                    color = WALL_COLOR
                elif (r, c) == self.maze.start:
                    color = START_COLOR
                elif (r, c) == self.maze.goal:
                    color = GOAL_COLOR
                else:
                    color = PATH_COLOR

                rect_id = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color, outline='')
                self.cells[(r, c)] = rect_id

    def color_cell(self, r, c, color):
        if (r, c) in self.cells:
            self.canvas.itemconfig(self.cells[(r, c)], fill=color)

    # ── Solving ──────────────────────────────────────────────────

    def solve(self):
        if not self.maze or self.animating:
            return
        self.clear_solution()
        algo_name = self.algo_var.get()
        algo_module = ALGORITHMS[algo_name]
        result = algo_module.solve(self.maze)

        self.save_result(algo_name, result)

        if not result['path']:
            self.update_stats(f"Algorithm: {algo_name}\nNo path found!")
            return

        self.show_stats(algo_name, result)
        self.animate(result)

    def solve_all(self):
        if not self.maze or self.animating:
            return
        self.clear_solution()

        stats_lines = []
        all_results = {}
        for algo_name, algo_module in ALGORITHMS.items():
            result = algo_module.solve(self.maze)
            all_results[algo_name] = result
            self.save_result(algo_name, result)

            stats_lines.append(f"=== {algo_name} ===")
            if result['path']:
                stats_lines.append(f"  Path Length : {len(result['path'])}")
                stats_lines.append(f"  Nodes Expl. : {result['nodes_explored']}")
                stats_lines.append(f"  Max Frontier: {result['max_frontier']}")
                stats_lines.append(f"  Time        : {result['execution_time']:.4f}s")
                if 'iterations' in result:
                    stats_lines.append(f"  Iterations  : {result['iterations']}")
            else:
                stats_lines.append("  No path found!")
            stats_lines.append("")

        self.update_stats("\n".join(stats_lines))

        # Draw all solution paths as colored lines
        for algo_name, result in all_results.items():
            if result['path']:
                self.draw_path_line(result['path'], ALGO_COLORS[algo_name])

    # ── Animation ────────────────────────────────────────────────

    def animate(self, result):
        self.animating = True
        visited = result['visited_order']
        path = result['path']
        delay = 30

        def step(i):
            if not self.animating:
                return
            if i < len(visited):
                r, c = visited[i]
                if (r, c) != self.maze.start and (r, c) != self.maze.goal:
                    self.color_cell(r, c, VISITED_COLOR)
                self._animation_id = self.root.after(delay, step, i + 1)
            else:
                for r, c in path:
                    if (r, c) != self.maze.start and (r, c) != self.maze.goal:
                        self.color_cell(r, c, SOLUTION_COLOR)
                self.animating = False

        step(0)

    def draw_path_line(self, path, color, width=3):
        if len(path) < 2:
            return
        points = []
        for r, c in path:
            x = c * self.cell_size + self.cell_size // 2
            y = r * self.cell_size + self.cell_size // 2
            points.extend([x, y])
        self.canvas.create_line(points, fill=color, width=width)
        # Ensure start/goal stay visible
        self.color_cell(*self.maze.start, START_COLOR)
        self.color_cell(*self.maze.goal, GOAL_COLOR)

    # ── Clear / Reset ────────────────────────────────────────────

    def clear_solution(self):
        if self.animating:
            self.animating = False
            if self._animation_id:
                self.root.after_cancel(self._animation_id)
                self._animation_id = None
        self.draw_maze()

    def reset(self):
        self.clear_solution()
        self.maze = None
        self.canvas.delete("all")
        self.cells = {}
        self.update_stats("")

    # ── Stats display ────────────────────────────────────────────

    def show_stats(self, algo_name, result):
        lines = [
            f"Algorithm   : {algo_name}",
            f"Path Length : {len(result['path'])}",
            f"Nodes Expl. : {result['nodes_explored']}",
            f"Max Frontier: {result['max_frontier']}",
            f"Time        : {result['execution_time']:.4f}s",
        ]
        if 'iterations' in result:
            lines.append(f"Iterations  : {result['iterations']}")
        self.update_stats("\n".join(lines))

    def update_stats(self, text):
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert("1.0", text)
        self.stats_text.config(state=tk.DISABLED)

    # ── CSV logging ──────────────────────────────────────────────

    def save_result(self, algo_name, result):
        file_path = 'results.csv'
        file_exists = os.path.exists(file_path)
        with open(file_path, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow([
                    'timestamp', 'maze_size', 'algorithm', 'path_length',
                    'nodes_explored', 'max_frontier', 'execution_time',
                    'iterations',
                ])
            writer.writerow([
                datetime.now().isoformat(),
                f"{self.maze.rows}x{self.maze.cols}",
                algo_name,
                len(result['path']),
                result['nodes_explored'],
                result['max_frontier'],
                f"{result['execution_time']:.6f}",
                result.get('iterations', ''),
            ])