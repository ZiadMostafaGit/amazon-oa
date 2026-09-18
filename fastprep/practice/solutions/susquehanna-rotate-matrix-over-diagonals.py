# Direct simulation: each turn maps every off-diagonal cell (r, c) to (c, n - 1 - r); diagonal cells stay.
from typing import List, Optional, Any


def rotateMatrixOverDiagonals(matrix: List[List[int]], turns: int) -> List[List[int]]:
    n = len(matrix)
    cur = [row[:] for row in matrix]
    for _ in range(turns):
        nxt = [row[:] for row in cur]
        for r in range(n):
            for c in range(n):
                if r == c or r + c == n - 1:
                    continue
                nxt[c][n - 1 - r] = cur[r][c]
        cur = nxt
    return cur
