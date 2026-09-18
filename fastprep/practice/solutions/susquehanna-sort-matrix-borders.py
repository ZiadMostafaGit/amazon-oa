# Ring decomposition: collect each k-border's cells in clockwise order, sort the values, write back.
from typing import List, Optional, Any


def _ring_cells(n: int, m: int, k: int) -> List[tuple]:
    top, bot, left, right = k, n - 1 - k, k, m - 1 - k
    cells = []
    for j in range(left, right + 1):
        cells.append((top, j))
    for i in range(top + 1, bot + 1):
        cells.append((i, right))
    if bot > top:
        for j in range(right - 1, left - 1, -1):
            cells.append((bot, j))
    if right > left:
        for i in range(bot - 1, top, -1):
            cells.append((i, left))
    return cells


def solution(matrix: List[List[int]]) -> List[List[int]]:
    n = len(matrix)
    if n == 0:
        return []
    m = len(matrix[0])
    res = [row[:] for row in matrix]
    k = 0
    while k <= n - 1 - k and k <= m - 1 - k:
        cells = _ring_cells(n, m, k)
        vals = sorted(res[i][j] for i, j in cells)
        for (i, j), v in zip(cells, vals):
            res[i][j] = v
        k += 1
    return res
