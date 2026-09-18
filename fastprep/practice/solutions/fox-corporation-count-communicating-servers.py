# Count per-row and per-column server totals, then keep servers whose row or column has another.
from typing import List


def countCommunicatingServers(grid: List[List[int]]) -> int:
    if not grid or not grid[0]:
        return 0
    rows = [sum(row) for row in grid]
    cols = [0] * len(grid[0])
    for row in grid:
        for c, v in enumerate(row):
            cols[c] += v
    total = 0
    for r, row in enumerate(grid):
        for c, v in enumerate(row):
            if v == 1 and (rows[r] > 1 or cols[c] > 1):
                total += 1
    return total
