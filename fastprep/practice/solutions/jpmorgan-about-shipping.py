# Prefix sums: the cost of a split is |prefix - suffix|, so scan every split once.
from typing import List, Optional, Any


def getMinimumOperations(quantity: List[int]) -> int:
    total = sum(quantity)
    prefix = 0
    best = None
    for i in range(len(quantity) - 1):
        prefix += quantity[i]
        diff = abs(2 * prefix - total)
        if best is None or diff < best:
            best = diff
    return best
