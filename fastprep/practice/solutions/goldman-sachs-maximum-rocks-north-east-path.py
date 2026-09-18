# Dynamic programming over the grid with a rolling row (moves north or east only).
from typing import List, Optional, Any


def maximumCollectedRocks(rocks: List[List[int]]) -> int:
    if not rocks or not rocks[0]:
        return 0
    cols = len(rocks[0])
    prev = [0] * cols
    for r, row in enumerate(rocks):
        cur = [0] * cols
        for c in range(cols):
            if r == 0 and c == 0:
                cur[c] = row[0]
            elif r == 0:
                cur[c] = cur[c - 1] + row[c]
            elif c == 0:
                cur[c] = prev[c] + row[c]
            else:
                best = prev[c] if prev[c] > cur[c - 1] else cur[c - 1]
                cur[c] = best + row[c]
        prev = cur
    return prev[cols - 1]
