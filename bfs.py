from collections import deque
import time


def solve(maze):
    start_time = time.time()
    start = maze.start
    goal = maze.goal

    queue = deque([start])
    visited = {start}
    parent = {start: None}
    visited_order = []
    max_frontier = 1

    while queue:
        max_frontier = max(max_frontier, len(queue))
        current = queue.popleft()
        visited_order.append(current)

        if current == goal:
            break

        for neighbor in maze.get_neighbors(*current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    # Reconstruct path
    path = []
    if goal in parent:
        current = goal
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()

    execution_time = time.time() - start_time
    return {
        'path': path,
        'visited_order': visited_order,
        'nodes_explored': len(visited_order),
        'max_frontier': max_frontier,
        'execution_time': execution_time,
    }
