# Separable Manhattan cost: weighted median on each axis independently.
from typing import List, Optional, Any


def _axis_cost(coords: List[int], people: List[int]) -> int:
    pairs = sorted(zip(coords, people))
    total = sum(people)
    half = (total + 1) // 2
    acc = 0
    median = pairs[0][0]
    for c, w in pairs:
        acc += w
        if acc >= half:
            median = c
            break
    return sum(w * abs(c - median) for c, w in pairs)


def minWeightedTravelCost(x: List[int], y: List[int], people: List[int]) -> int:
    return _axis_cost(x, people) + _axis_cost(y, people)
