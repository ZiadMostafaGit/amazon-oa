# 2D prefix sums, then each output cell is one clipped rectangle query.
from typing import List, Optional, Any


def matrixRegionSum(matrix: List[List[int]], r: int) -> List[List[int]]:
    m = len(matrix)
    n = len(matrix[0]) if m else 0
    pre = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        row = matrix[i]
        prev_row = pre[i]
        cur = pre[i + 1]
        running = 0
        for j in range(n):
            running += row[j]
            cur[j + 1] = prev_row[j + 1] + running
    out = [[0] * n for _ in range(m)]
    for i in range(m):
        r1 = max(0, i - r)
        r2 = min(m - 1, i + r)
        top = pre[r1]
        bot = pre[r2 + 1]
        line = out[i]
        for j in range(n):
            c1 = max(0, j - r)
            c2 = min(n - 1, j + r) + 1
            line[j] = bot[c2] - bot[c1] - top[c2] + top[c1]
    return out
