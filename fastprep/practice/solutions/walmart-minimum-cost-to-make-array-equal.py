# Weighted median: sort by value and pick the target where cumulative weight reaches half.
from typing import List, Optional, Any


def minCost(nums: List[int], cost: List[int]) -> int:
    pairs = sorted(zip(nums, cost))
    total = sum(cost)
    half = (total + 1) // 2
    run = 0
    target = pairs[0][0]
    for v, w in pairs:
        run += w
        if run >= half:
            target = v
            break
    return sum(abs(v - target) * w for v, w in pairs)
