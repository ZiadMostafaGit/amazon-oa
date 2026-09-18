# Iterative DFS flood fill over the grid, counting each unvisited land component once.
from typing import List


def countIslands(grid: List[List[int]]) -> int:
    if not grid or not grid[0]:
        return 0
    rows = len(grid)
    cols = len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1 or seen[r][c]:
                continue
            count += 1
            stack = [(r, c)]
            seen[r][c] = True
            while stack:
                cr, cc = stack.pop()
                for nr, nc in ((cr - 1, cc), (cr + 1, cc), (cr, cc - 1), (cr, cc + 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and not seen[nr][nc] and grid[nr][nc] == 1:
                        seen[nr][nc] = True
                        stack.append((nr, nc))
    return count
