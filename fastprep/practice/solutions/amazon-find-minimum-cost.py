# Circular redistribution with a single fixed direction: edge flows are prefix sums shifted by a constant, minimized at min/max prefix.
from typing import List, Optional, Any


def findMinimumCost(products: List[int]) -> int:
    n = len(products)
    total = sum(products)
    avg = total // n

    prefix = 0
    prefix_sum = 0
    lo = None
    hi = None
    for value in products:
        prefix += value - avg
        prefix_sum += prefix
        if lo is None or prefix < lo:
            lo = prefix
        if hi is None or prefix > hi:
            hi = prefix

    forward = prefix_sum - n * lo
    backward = n * hi - prefix_sum
    return min(forward, backward)
