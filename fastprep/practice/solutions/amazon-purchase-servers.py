# Sort each cost class descending, build prefix sums, and binary search the cost-2 count per cost-1 count.
from typing import List, Optional, Any
from bisect import bisect_left


def minCostToPurchaseServers(power: List[int], cost: List[int], target: int) -> int:
    if target <= 0:
        return 0
    ones = []
    twos = []
    for p, c in zip(power, cost):
        if p <= 0:
            continue
        if c == 1:
            ones.append(p)
        else:
            twos.append(p)
    ones.sort(reverse=True)
    twos.sort(reverse=True)

    p1 = [0]
    for v in ones:
        p1.append(p1[-1] + v)
    p2 = [0]
    for v in twos:
        p2.append(p2[-1] + v)

    if p1[-1] + p2[-1] < target:
        return -1

    best = None
    for a in range(len(p1)):
        need = target - p1[a]
        if need <= 0:
            b = 0
        else:
            if p2[-1] < need:
                continue
            b = bisect_left(p2, need)
        total = a + 2 * b
        if best is None or total < best:
            best = total
    return best if best is not None else -1
