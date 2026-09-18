# Closed-form minimum skips per warehouse (residue arithmetic), then greedily buy the cheapest warehouses.
from typing import List, Optional, Any


def maxPoints(inventory: List[int], dispatch1: int, dispatch2: int, skips: int) -> int:
    s = dispatch1 + dispatch2
    costs = []
    for v in inventory:
        g = (v - 1) % s
        costs.append(g // dispatch1)
    costs.sort()
    budget = skips
    points = 0
    for c in costs:
        if c > budget:
            break
        budget -= c
        points += 1
    return points
