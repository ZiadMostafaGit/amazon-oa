# 2D prefix sums, then scan side lengths from largest to smallest checking every square.
from typing import List, Optional, Any


def largestSquareSubgrid(grid: List[List[int]], maxSum: int) -> int:
    if not grid or not grid[0]:
        return 0
    rows = len(grid)
    cols = len(grid[0])
    pre = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(rows):
        row = grid[r]
        pr = pre[r]
        cr = pre[r + 1]
        running = 0
        for c in range(cols):
            running += row[c]
            cr[c + 1] = pr[c + 1] + running

    for k in range(min(rows, cols), 0, -1):
        ok = True
        for r in range(rows - k + 1):
            top = pre[r]
            bot = pre[r + k]
            for c in range(cols - k + 1):
                if bot[c + k] - bot[c] - top[c + k] + top[c] > maxSum:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            return k
    return 0
