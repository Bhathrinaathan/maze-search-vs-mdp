import random


class Maze:
    def __init__(self, rows=10, cols=10):
        self.rows = rows
        self.cols = cols
        self.height = 2 * rows + 1
        self.width = 2 * cols + 1
        self.grid = [[1] * self.width for _ in range(self.height)]
        self.start = (1, 1)
        self.goal = (self.height - 2, self.width - 2)

    def generate(self):
        """Generate maze using iterative recursive backtracker."""
        self.grid = [[1] * self.width for _ in range(self.height)]
        visited = [[False] * self.cols for _ in range(self.rows)]

        def cell_to_grid(r, c):
            return (2 * r + 1, 2 * c + 1)

        # Start from cell (0, 0)
        stack = [(0, 0)]
        visited[0][0] = True
        gr, gc = cell_to_grid(0, 0)
        self.grid[gr][gc] = 0

        while stack:
            r, c = stack[-1]
            gr, gc = cell_to_grid(r, c)

            # Find unvisited neighbors
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(directions)

            found = False
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and not visited[nr][nc]:
                    visited[nr][nc] = True
                    ngr, ngc = cell_to_grid(nr, nc)
                    self.grid[ngr][ngc] = 0
                    # Remove wall between current and neighbor
                    self.grid[gr + dr][gc + dc] = 0
                    stack.append((nr, nc))
                    found = True
                    break

            if not found:
                stack.pop()

        self._add_extra_paths()
        self.start = (1, 1)
        self.goal = (self.height - 2, self.width - 2)

    def _add_extra_paths(self):
        """Remove 2-4 extra walls to create multiple solution paths."""
        candidates = []
        for r in range(1, self.height - 1):
            for c in range(1, self.width - 1):
                if self.grid[r][c] == 1:
                    # Horizontal wall between two path cells
                    if r % 2 == 0 and c % 2 == 1:
                        if self.grid[r - 1][c] == 0 and self.grid[r + 1][c] == 0:
                            candidates.append((r, c))
                    # Vertical wall between two path cells
                    elif r % 2 == 1 and c % 2 == 0:
                        if self.grid[r][c - 1] == 0 and self.grid[r][c + 1] == 0:
                            candidates.append((r, c))

        random.shuffle(candidates)
        num_to_remove = min(random.randint(2, 4), len(candidates))
        for i in range(num_to_remove):
            r, c = candidates[i]
            self.grid[r][c] = 0

    def get_neighbors(self, r, c):
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.height and 0 <= nc < self.width and self.grid[nr][nc] == 0:
                neighbors.append((nr, nc))
        return neighbors


#This code implements the recursive backtracker maze-generation algorithm (iterative DFS variant), as described by Buck and Sweigart, with post-processing to remove 2-4 internal walls for multiple solution paths.
# J. Buck, "Maze Generation: Recursive Backtracking," Buckblog, 2010.
