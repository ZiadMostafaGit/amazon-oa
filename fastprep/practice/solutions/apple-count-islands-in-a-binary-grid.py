# Iterative DFS flood fill over the grid, marking visited land in place.
from typing import List, Optional, Any


def countIslands(grid: List[List[int]]) -> int:
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
    for sr in range(rows):
        for sc in range(cols):
            if grid[sr][sc] != 1:
                continue
            count += 1
            stack = [(sr, sc)]
            grid[sr][sc] = 0
            while stack:
                r, c = stack.pop()
                for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                        grid[nr][nc] = 0
                        stack.append((nr, nc))
    return count
