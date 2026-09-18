# 2D prefix sums, then one clipped rectangle query per cell.
from typing import List, Optional, Any


def centeredSubmatrixSums(matrix: List[List[int]], k: int) -> List[List[int]]:
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    r = (k - 1) // 2
    pre = [[0] * (cols + 1) for _ in range(rows + 1)]
    for i in range(rows):
        row = matrix[i]
        prev = pre[i]
        cur = pre[i + 1]
        run = 0
        for j in range(cols):
            run += row[j]
            cur[j + 1] = prev[j + 1] + run
    out = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        r1 = i - r
        if r1 < 0:
            r1 = 0
        r2 = i + r
        if r2 > rows - 1:
            r2 = rows - 1
        top = pre[r1]
        bot = pre[r2 + 1]
        orow = out[i]
        for j in range(cols):
            c1 = j - r
            if c1 < 0:
                c1 = 0
            c2 = j + r
            if c2 > cols - 1:
                c2 = cols - 1
            orow[j] = bot[c2 + 1] - bot[c1] - top[c2 + 1] + top[c1]
    return out
