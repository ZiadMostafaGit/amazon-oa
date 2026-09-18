# Backward DP (dungeon-game style): min health needed before entering each cell, allowing zero.
from typing import List, Optional, Any


def minimumStartingHealth(grid: List[List[int]]) -> int:
    rows = len(grid)
    cols = len(grid[0])
    INF = float("inf")
    # need[j] = minimum health required just before entering cell (i, j)
    need = [INF] * (cols + 1)
    for i in range(rows - 1, -1, -1):
        new = [INF] * (cols + 1)
        for j in range(cols - 1, -1, -1):
            if i == rows - 1 and j == cols - 1:
                after = 0
            else:
                after = min(need[j], new[j + 1])
            v = after - grid[i][j]
            new[j] = v if v > 0 else 0
        need = new
    return need[0]
