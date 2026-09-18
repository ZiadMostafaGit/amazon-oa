# Binary search the water level; since a^2+b^2 <= (a+b)^2, landing on every un-submerged rock is optimal.
from typing import List, Optional, Any


def maxWaterHeight(width: int, numRocks: int, maxJump: int, maxEnergy: int, x: List[int], heights: List[int]) -> int:
    CAP = 10 ** 9
    order = sorted(range(len(x)), key=lambda i: x[i])
    xs = [x[i] for i in order]
    hs = [heights[i] for i in order]

    def feasible(level: int) -> bool:
        prev = 0
        energy = 0
        for i in range(len(xs)):
            if hs[i] < level:
                continue
            gap = xs[i] - prev
            if gap > maxJump:
                return False
            energy += gap * gap
            if energy > maxEnergy:
                return False
            prev = xs[i]
        gap = width - prev
        if gap > maxJump:
            return False
        energy += gap * gap
        return energy <= maxEnergy

    if not feasible(0):
        return -1
    lo, hi = 0, CAP
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo
