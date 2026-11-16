# Maze Pathfinding: Classical Search vs MDP Planning

Six maze-solving algorithms, one maze generator, an interactive Tkinter visualiser, and a benchmark across maze sizes from 10×10 to 100×100.

| Family | Algorithms |
|---|---|
| Uninformed search | Breadth-First Search, Depth-First Search |
| Informed search | A\* with Manhattan heuristic, A\* with Euclidean heuristic |
| Markov Decision Process | Value Iteration, Policy Iteration |

Built for the Artificial Intelligence module (CS7IS2), MSc Computer Science (Intelligent Systems), Trinity College Dublin, 2026.

## Headline results (100×100 maze, `results.csv`)

| Algorithm | Path length | Nodes / states explored | Time |
|---|---|---|---|
| BFS | 7,769 | 18,549 | 0.012 s |
| DFS | 7,769 | 12,711 | 0.008 s |
| A\* Manhattan | 7,769 | 18,411 | 0.017 s |
| A\* Euclidean | 7,769 | 18,429 | 0.020 s |
| Value Iteration | 7,769 | 20,002 (4,083 sweeps) | 39.0 s |
| Policy Iteration | 7,769 | 20,002 (4,131 sweeps) | 80.1 s |

- **Every method finds an optimal path**, but the MDP planners pay for it: Value Iteration is ~3,200× slower than BFS and Policy Iteration ~6,600× slower on the largest maze. Planning over every state is the wrong tool for a deterministic, single-goal problem, and this makes the trade-off concrete.
- **A\* explores almost as much as BFS here.** Perfect mazes with a few extra openings have long, winding corridors, so the heuristic rarely gets to prune; A\*'s advantage shows up on open grids, not on labyrinths.
- **DFS looks good on this maze but is not reliable.** It happens to find the optimal 7,769-step path on the 100×100 instance and explores fewest nodes, but on smaller instances in `results.csv` it returns longer paths (85 vs 73 on 10×10). It has no optimality guarantee.
- **Policy Iteration needs about as many sweeps as Value Iteration** (4,131 vs 4,083) because each policy-evaluation step is itself iterated to convergence on a 20,002-state grid.

## Repository layout

```
main.py               # Tkinter app: generate a maze, pick an algorithm, watch it solve
maze.py               # iterative recursive-backtracker generator (+2–4 extra openings)
bfs.py, dfs.py        # uninformed search
astar_manhattan.py    # A* variants, shared open/closed-set implementation
astar_euclidean.py
value_iteration.py    # MDP planners over the open-cell state space
policy_iteration.py
evaluation.py         # runs every algorithm over several sizes, writes results.csv + plots
gui.py                # drawing and animation helpers
results.csv           # recorded runs (path length, nodes explored, max frontier, time, iterations)
analysis_outputs/     # generated charts
```

Each algorithm module exposes `solve(maze) -> dict` returning the path, visit order, nodes explored, maximum frontier size and execution time, so adding a new algorithm is one file.

## Running it

```bash
pip install pandas matplotlib numpy     # tkinter ships with Python

python main.py          # interactive visualiser
python evaluation.py    # benchmark and charts
```

## Design notes

- Mazes are perfect mazes from an iterative recursive backtracker, then 2–4 random walls are removed so there is more than one route. That is what lets BFS and DFS disagree and gives the MDP planners real choices.
- The MDP formulation uses deterministic transitions with a reward of −1 per step, −10 for walking into a wall and +1,000 at the goal, a discount of 0.999 (high so the goal reward still reaches the far corner of a 100×100 grid), and a convergence threshold of 0.1 on the largest value change per sweep.
- Timings are wall-clock on a single core; see `results.csv` for every recorded run including smaller sizes.
