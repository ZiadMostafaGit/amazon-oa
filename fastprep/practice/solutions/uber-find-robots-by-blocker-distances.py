# Directional scan: for each robot walk in each of the 4 directions counting steps
# until the first blocker or the first out-of-bounds position (that step included).
from typing import List, Optional, Any


def findRobots(grid: List[str], query: List[int]) -> List[List[int]]:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    def dist(r: int, c: int, dr: int, dc: int) -> int:
        steps = 0
        rr, cc = r, c
        while True:
            rr += dr
            cc += dc
            steps += 1
            if rr < 0 or rr >= rows or cc < 0 or cc >= cols:
                return steps
            if grid[rr][cc] == 'X':
                return steps

    want_left, want_top, want_bottom, want_right = query
    res: List[List[int]] = []
    for r in range(rows):
        row = grid[r]
        for c in range(cols):
            if row[c] != 'O':
                continue
            if dist(r, c, 0, -1) != want_left:
                continue
            if dist(r, c, -1, 0) != want_top:
                continue
            if dist(r, c, 1, 0) != want_bottom:
                continue
            if dist(r, c, 0, 1) != want_right:
                continue
            res.append([r, c])
    return res
