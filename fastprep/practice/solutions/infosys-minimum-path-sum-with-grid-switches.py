# Grid DP with a layer: best[g][r][c] for g in {grid1, grid2}; after entering a cell, allow one switch there.
from typing import List


def minPathSumWithGridSwitches(grid1: List[List[int]], grid2: List[List[int]], switchCost: int) -> int:
    rows, cols = len(grid1), len(grid1[0])
    INF = float("inf")
    g = (grid1, grid2)
    prev = [[INF] * cols for _ in range(2)]
    for r in range(rows):
        cur = [[INF] * cols for _ in range(2)]
        for c in range(cols):
            for k in range(2):
                if r == 0 and c == 0:
                    come = 0
                else:
                    come = min(prev[k][c] if r else INF, cur[k][c - 1] if c else INF)
                cur[k][c] = come + g[k][r][c]
            a, b = cur[0][c], cur[1][c]
            cur[0][c] = min(a, b + switchCost)
            cur[1][c] = min(b, a + switchCost)
        prev = cur
    return min(prev[0][-1], prev[1][-1])
