# Greedy: per row keep only its top limit[i] values, then take the x largest of that pool.
from typing import List, Optional, Any


def findMaxValue(limit: List[int], matrix: List[List[int]], x: int) -> int:
    pool = []
    for i, row in enumerate(matrix):
        k = limit[i]
        if k <= 0:
            continue
        top = sorted(row, reverse=True)[:k]
        pool.extend(top)
    if len(pool) < x:
        return -1
    pool.sort(reverse=True)
    return sum(pool[:x])
