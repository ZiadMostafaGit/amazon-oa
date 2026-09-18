# Manhattan distance separates into rows and columns; the median minimizes 1-D sum.
from typing import List, Optional, Any


def minTotalDistance(grid: List[List[int]]) -> int:
    rows = []
    cols = []
    for r, row in enumerate(grid):
        for c, v in enumerate(row):
            if v == 1:
                rows.append(r)
                cols.append(c)
    if not rows:
        return 0
    cols.sort()

    def cost(vals: List[int]) -> int:
        m = vals[len(vals) // 2]
        return sum(abs(v - m) for v in vals)

    return cost(rows) + cost(cols)
