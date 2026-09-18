# Multi-source BFS: one BFS per building, accumulating distance sums and reach counts per empty cell.
from typing import List, Optional, Any
from collections import deque


def shortestDistance(grid: List[List[int]]) -> int:
    if not grid or not grid[0]:
        return -1
    rows, cols = len(grid), len(grid[0])
    total = [[0] * cols for _ in range(rows)]
    reach = [[0] * cols for _ in range(rows)]
    buildings = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1:
                continue
            buildings += 1
            seen = [[False] * cols for _ in range(rows)]
            seen[r][c] = True
            q = deque([(r, c, 0)])
            while q:
                cr, cc, d = q.popleft()
                for nr, nc in ((cr - 1, cc), (cr + 1, cc), (cr, cc - 1), (cr, cc + 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and not seen[nr][nc] and grid[nr][nc] == 0:
                        seen[nr][nc] = True
                        total[nr][nc] += d + 1
                        reach[nr][nc] += 1
                        q.append((nr, nc, d + 1))

    best = -1
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0 and reach[r][c] == buildings:
                if best == -1 or total[r][c] < best:
                    best = total[r][c]
    return best
