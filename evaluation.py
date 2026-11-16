

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

matplotlib.use('Agg')

# Load Data

OUTPUT_DIR = 'analysis_outputs'
os.makedirs(OUTPUT_DIR, exist_ok=True)


df = pd.read_csv("results.csv")
df['execution_time_ms'] = df['execution_time'] * 1000  # Convert to milliseconds
df['iterations'] = df['iterations'].fillna(0).astype(int)

# Ordering for consistent plots
size_order = ['10x10', '20x20', '50x50', '75x75', '100x100']
algo_order = ['BFS', 'DFS', 'A* Manhattan', 'A* Euclidean', 'Value Iteration', 'Policy Iteration']
search_algos = ['BFS', 'DFS', 'A* Manhattan', 'A* Euclidean']
mdp_algos = ['Value Iteration', 'Policy Iteration']

df['maze_size'] = pd.Categorical(df['maze_size'], categories=size_order, ordered=True)
df['algorithm'] = pd.Categorical(df['algorithm'], categories=algo_order, ordered=True)
df = df.sort_values(['maze_size', 'algorithm'])

# Consistent style
COLORS = {
    'BFS': '#2196F3',
    'DFS': '#4CAF50',
    'A* Manhattan': '#FF9800',
    'A* Euclidean': '#F44336',
    'Value Iteration': '#9C27B0',
    'Policy Iteration': '#607D8B'
}

plt.rcParams.update({
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 11,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.grid': True,
    'grid.alpha': 0.3,
})

def save_fig(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {path}")

# Execution Time — All Algorithms (Grouped Bar)

def plot_execution_time_all():
    fig, ax = plt.subplots(figsize=(10, 5))
    sizes = size_order
    n_algos = len(algo_order)
    x = np.arange(len(sizes))
    width = 0.12

    for i, algo in enumerate(algo_order):
        subset = df[df['algorithm'] == algo]
        times = [subset[subset['maze_size'] == s]['execution_time_ms'].values[0] for s in sizes]
        offset = (i - n_algos / 2 + 0.5) * width
        bars = ax.bar(x + offset, times, width, label=algo, color=COLORS[algo])
        for bar, val in zip(bars, times):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                    f'{val:.2f}', ha='center', va='bottom', fontsize=7)

    ax.set_xlabel('Maze Size')
    ax.set_ylabel('Execution Time (ms)')
    ax.set_title('Execution Time — All Algorithms')
    ax.set_xticks(x)
    ax.set_xticklabels(sizes)
    ax.legend(fontsize=8, ncol=3)
    ax.set_yscale('log')
    ax.set_ylabel('Execution Time (ms) — log scale')
    fig.tight_layout()
    save_fig(fig, 'execution_time_all.png')



# Nodes Explored — All Algorithms


def plot_nodes_explored():
    fig, ax = plt.subplots(figsize=(10, 5))
    sizes = size_order
    n_algos = len(algo_order)
    x = np.arange(len(sizes))
    width = 0.12

    for i, algo in enumerate(algo_order):
        subset = df[df['algorithm'] == algo]
        nodes = [subset[subset['maze_size'] == s]['nodes_explored'].values[0] for s in sizes]
        offset = (i - n_algos / 2 + 0.5) * width
        bars = ax.bar(x + offset, nodes, width, label=algo, color=COLORS[algo])
        for bar, val in zip(bars, nodes):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                    str(val), ha='center', va='bottom', fontsize=7)

    ax.set_xlabel('Maze Size')
    ax.set_ylabel('Nodes Explored')
    ax.set_title('Nodes Explored — All Algorithms')
    ax.set_xticks(x)
    ax.set_xticklabels(sizes)
    ax.legend(fontsize=8, ncol=3)
    fig.tight_layout()
    save_fig(fig, 'nodes_explored_all.png')



# Path Length Comparison

def plot_path_length():
    fig, ax = plt.subplots(figsize=(10, 5))
    sizes = size_order
    n_algos = len(algo_order)
    x = np.arange(len(sizes))
    width = 0.12

    for i, algo in enumerate(algo_order):
        subset = df[df['algorithm'] == algo]
        lengths = [subset[subset['maze_size'] == s]['path_length'].values[0] for s in sizes]
        offset = (i - n_algos / 2 + 0.5) * width
        bars = ax.bar(x + offset, lengths, width, label=algo, color=COLORS[algo])
        for bar, val in zip(bars, lengths):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                    str(val), ha='center', va='bottom', fontsize=7)

    ax.set_xlabel('Maze Size')
    ax.set_ylabel('Path Length (steps)')
    ax.set_title('Path Length — All Algorithms')
    ax.set_xticks(x)
    ax.set_xticklabels(sizes)
    ax.legend(fontsize=8, ncol=3)
    fig.tight_layout()
    save_fig(fig, 'path_length.png')


# Search vs MDP — Time Scaling (Line Plot)


def plot_search_vs_mdp_time():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    sizes_num = [10, 20, 50, 75, 100]

    # Left: Search algorithms
    for algo in search_algos:
        subset = df[df['algorithm'] == algo]
        times = [subset[subset['maze_size'] == s]['execution_time_ms'].values[0] for s in size_order]
        ax1.plot(sizes_num, times, 'o-', label=algo, color=COLORS[algo], linewidth=2, markersize=7)

    ax1.set_xlabel('Maze Size (N in NxN)')
    ax1.set_ylabel('Execution Time (ms)')
    ax1.set_title('Search Algorithms — Time Scaling')
    ax1.legend()
    ax1.set_xticks(sizes_num)

    # Right: MDP algorithms
    for algo in mdp_algos:
        subset = df[df['algorithm'] == algo]
        times = [subset[subset['maze_size'] == s]['execution_time_ms'].values[0] for s in size_order]
        ax2.plot(sizes_num, times, 's-', label=algo, color=COLORS[algo], linewidth=2, markersize=7)

    ax2.set_xlabel('Maze Size (N in NxN)')
    ax2.set_ylabel('Execution Time (ms)')
    ax2.set_title('MDP Algorithms — Time Scaling')
    ax2.legend()
    ax2.set_xticks(sizes_num)

    fig.suptitle('Search vs MDP — Execution Time Scaling', fontsize=14, fontweight='bold')
    fig.tight_layout()
    save_fig(fig, 'search_vs_mdp_time.png')


# MDP Iterations & Time

def plot_mdp_details():
    mdp_df = df[df['algorithm'].isin(mdp_algos)]

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    sizes_num = [10, 20, 50, 75, 100]

    # Iterations
    for algo in mdp_algos:
        subset = mdp_df[mdp_df['algorithm'] == algo]
        vals = [subset[subset['maze_size'] == s]['iterations'].values[0] for s in size_order]
        axes[0].plot(sizes_num, vals, 's-', label=algo, color=COLORS[algo], linewidth=2, markersize=7)
        for x, v in zip(sizes_num, vals):
            axes[0].annotate(str(v), (x, v), textcoords="offset points",
                             xytext=(0, 8), ha='center', fontsize=9)
    axes[0].set_title('Iterations to Converge')
    axes[0].set_xlabel('Maze Size (N)')
    axes[0].set_ylabel('Iterations')
    axes[0].legend()
    axes[0].set_xticks(sizes_num)

    # Execution time
    for algo in mdp_algos:
        subset = mdp_df[mdp_df['algorithm'] == algo]
        vals = [subset[subset['maze_size'] == s]['execution_time_ms'].values[0] for s in size_order]
        axes[1].plot(sizes_num, vals, 's-', label=algo, color=COLORS[algo], linewidth=2, markersize=7)
        for x, v in zip(sizes_num, vals):
            axes[1].annotate(f'{v:.1f}', (x, v), textcoords="offset points",
                             xytext=(0, 8), ha='center', fontsize=9)
    axes[1].set_title('Execution Time (ms)')
    axes[1].set_xlabel('Maze Size (N)')
    axes[1].set_ylabel('Time (ms)')
    axes[1].legend()
    axes[1].set_xticks(sizes_num)

    # Nodes explored (states)
    for algo in mdp_algos:
        subset = mdp_df[mdp_df['algorithm'] == algo]
        vals = [subset[subset['maze_size'] == s]['nodes_explored'].values[0] for s in size_order]
        axes[2].plot(sizes_num, vals, 's-', label=algo, color=COLORS[algo], linewidth=2, markersize=7)
        for x, v in zip(sizes_num, vals):
            axes[2].annotate(str(v), (x, v), textcoords="offset points",
                             xytext=(0, 8), ha='center', fontsize=9)
    axes[2].set_title('States Processed')
    axes[2].set_xlabel('Maze Size (N)')
    axes[2].set_ylabel('States')
    axes[2].legend()
    axes[2].set_xticks(sizes_num)

    fig.suptitle('MDP Algorithms — Detailed Comparison', fontsize=13, fontweight='bold')
    fig.tight_layout()
    save_fig(fig, 'mdp_details.png')



# Time Ratio — How much slower is MDP vs Search


def plot_time_ratio():
    fig, ax = plt.subplots(figsize=(8, 5))
    sizes_num = [10, 20, 50, 75, 100]

    # Use BFS as baseline (fastest reliable search)
    bfs_times = []
    for s in size_order:
        t = df[(df['algorithm'] == 'BFS') & (df['maze_size'] == s)]['execution_time_ms'].values[0]
        bfs_times.append(t)

    for algo in algo_order:
        if algo == 'BFS':
            continue
        times = []
        for s in size_order:
            t = df[(df['algorithm'] == algo) & (df['maze_size'] == s)]['execution_time_ms'].values[0]
            times.append(t)
        ratios = [t / b for t, b in zip(times, bfs_times)]
        marker = 's' if algo in mdp_algos else 'o'
        ax.plot(sizes_num, ratios, f'{marker}-', label=algo, color=COLORS[algo],
                linewidth=2, markersize=7)
        for x, r in zip(sizes_num, ratios):
            ax.annotate(f'{r:.1f}x', (x, r), textcoords="offset points",
                        xytext=(5, 5), fontsize=8)

    ax.axhline(y=1, color='gray', linestyle='--', alpha=0.5, label='BFS baseline (1x)')
    ax.set_xlabel('Maze Size (N)')
    ax.set_ylabel('Time Ratio vs BFS')
    ax.set_title('Execution Time Relative to BFS')
    ax.set_yscale('log')
    ax.legend(fontsize=8)
    ax.set_xticks(sizes_num)
    fig.tight_layout()
    save_fig(fig, 'time_ratio_vs_bfs.png')

if __name__ == '__main__':
    plot_execution_time_all()
    plot_nodes_explored()
    plot_path_length()
    plot_search_vs_mdp_time()
    plot_mdp_details()
    plot_time_ratio()
