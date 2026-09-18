# DP reachability over the sub-rectangle between source and destination, moving only right/down.
from typing import List, Optional, Any


def solve(grid: List[str], source: List[int], destination: List[int]) -> bool:
    if not grid:
        return False
    rows = len(grid)
    sr, sc = source[0], source[1]
    dr, dc = destination[0], destination[1]
    if not (0 <= sr < rows and 0 <= dr < rows):
        return False
    if not (0 <= sc < len(grid[sr]) and 0 <= dc < len(grid[dr])):
        return False
    # Only right and down moves, so the destination must be weakly below-right.
    if dr < sr or dc < sc:
        return False

    def open_cell(r: int, c: int) -> bool:
        row = grid[r]
        return c < len(row) and row[c] != 'X'

    if not open_cell(sr, sc) or not open_cell(dr, dc):
        return False

    width = dc - sc + 1
    reach = [False] * width
    reach[0] = True
    for r in range(sr, dr + 1):
        for j in range(width):
            c = sc + j
            if not open_cell(r, c):
                reach[j] = False
            elif j > 0 and reach[j - 1]:
                reach[j] = True
        if not any(reach):
            return False
    return reach[width - 1]
