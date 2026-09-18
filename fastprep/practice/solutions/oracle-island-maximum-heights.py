# Iterative flood fill (BFS with a stack) per island, scanning cells in row-major order.
from typing import List, Optional, Any


def islandMaximumHeights(grid: List[List[int]]) -> List[int]:
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    result = []

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] <= 0 or seen[r][c]:
                continue
            seen[r][c] = True
            stack = [(r, c)]
            best = grid[r][c]
            while stack:
                cr, cc = stack.pop()
                if grid[cr][cc] > best:
                    best = grid[cr][cc]
                for nr, nc in ((cr - 1, cc), (cr + 1, cc), (cr, cc - 1), (cr, cc + 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and not seen[nr][nc] and grid[nr][nc] > 0:
                        seen[nr][nc] = True
                        stack.append((nr, nc))
            result.append(best)

    return result
