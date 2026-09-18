# Iterative DFS over a visited set counting 4-connected components of '1' cells.
from typing import List, Optional, Any


def countIslands(grid: List[str]) -> int:
    if not grid:
        return 0
    rows = len(grid)
    cols = len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and not seen[r][c]:
                count += 1
                stack = [(r, c)]
                seen[r][c] = True
                while stack:
                    x, y = stack.pop()
                    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                        if 0 <= nx < rows and 0 <= ny < cols and not seen[nx][ny] and grid[nx][ny] == '1':
                            seen[nx][ny] = True
                            stack.append((nx, ny))
    return count
