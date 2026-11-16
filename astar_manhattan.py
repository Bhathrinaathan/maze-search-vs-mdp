import heapq
import time


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def solve(maze):
    start_time = time.time()
    start = maze.start
    goal = maze.goal

    counter = 0
    open_set = [(heuristic(start, goal), counter, start)]
    g_score = {start: 0}
    parent = {start: None}
    visited_order = []
    closed = set()
    max_frontier = 1

    while open_set:
        max_frontier = max(max_frontier, len(open_set))
        f, _, current = heapq.heappop(open_set)

        if current in closed:
            continue
        closed.add(current)
        visited_order.append(current)

        if current == goal:
            break

        for neighbor in maze.get_neighbors(*current):
            if neighbor in closed:
                continue
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                parent[neighbor] = current
                counter += 1
                heapq.heappush(open_set, (f_score, counter, neighbor))

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
