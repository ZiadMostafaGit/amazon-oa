# Iterative DFS flood fill over the grid, counting connected components of '1'.
from typing import List, Optional, Any


def numIslands(grid: List[str]) -> int:
    if not grid or not grid[0]:
        return 0
    rows = len(grid)
    cols = len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    count = 0
    for r in range(rows):
        row = grid[r]
        for c in range(cols):
            if row[c] != '1' or seen[r][c]:
                continue
            count += 1
            stack = [(r, c)]
            seen[r][c] = True
            while stack:
                i, j = stack.pop()
                for ni, nj in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
                    if 0 <= ni < rows and 0 <= nj < cols and not seen[ni][nj] and grid[ni][nj] == '1':
                        seen[ni][nj] = True
                        stack.append((ni, nj))
    return count
