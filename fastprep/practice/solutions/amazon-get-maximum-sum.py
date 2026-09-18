# Aggregate health per server type in a hash map, then sum the k largest type totals.
from typing import List, Optional, Any


def getMaximumSum(health: List[int], serverType: List[int], k: int) -> int:
    totals = {}
    for h, t in zip(health, serverType):
        totals[t] = totals.get(t, 0) + h
    sums = sorted(totals.values(), reverse=True)
    return sum(sums[:k])
