import time


def solve(maze):
    start_time = time.time()
    start = maze.start
    goal = maze.goal

    # Collect all path cells as states
    states = []
    for r in range(maze.height):
        for c in range(maze.width):
            if maze.grid[r][c] == 0:
                states.append((r, c))

    state_set = set(states)
    actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    gamma = 0.999  # Higher discount for better long-term planning in large mazes
    threshold = 0.1  # More relaxed threshold
    max_iterations = 100000
    goal_reward = 1000.0  # Larger reward for large mazes

    V = {s: 0.0 for s in states}

    iterations = 0
    while iterations < max_iterations:
        delta = 0
        iterations += 1
        for s in states:
            if s == goal:
                continue
            max_val = float('-inf')
            for dr, dc in actions:
                ns = (s[0] + dr, s[1] + dc)
                if ns in state_set:
                    reward = goal_reward if ns == goal else -1.0
                    val = reward + gamma * V[ns]
                else:
                    val = -10.0 + gamma * V[s]  # hit wall penalty
                max_val = max(max_val, val)
            delta = max(delta, abs(max_val - V[s]))
            V[s] = max_val
        if delta < threshold:
            break

    # Extract path by following greedy policy
    visited_order = list(states)  # all states were considered
    path = [start]
    current = start
    max_path_length = len(states) * 10  # Allow much longer paths

    while current != goal and len(path) < max_path_length:
        best_next = None
        best_val = float('-inf')
        for dr, dc in actions:
            ns = (current[0] + dr, current[1] + dc)
            if ns in state_set:
                reward = goal_reward if ns == goal else -1.0
                val = reward + gamma * V[ns]
                if val > best_val:
                    best_val = val
                    best_next = ns
        if best_next is None:
            break
        current = best_next
        path.append(current)
        # Detect cycles - if path is too long and not making progress
        if len(path) > 1000 and len(set(path[-100:])) < 50:
            break

    execution_time = time.time() - start_time
    return {
        'path': path if current == goal else [],
        'visited_order': visited_order,
        'nodes_explored': len(visited_order),
        'max_frontier': len(states),
        'execution_time': execution_time,
        'iterations': iterations,
    }
