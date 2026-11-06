# Keep the cheapest cost so far ending in each color; each house adds its cost to the best of the other two.
from typing import List, Optional, Any


def minPaintCost(costs: List[List[int]]) -> int:
    a, b, c = 0, 0, 0
    for x, y, z in costs:
        a, b, c = x + min(b, c), y + min(a, c), z + min(a, b)
    return min(a, b, c)
