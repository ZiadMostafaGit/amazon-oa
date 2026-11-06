# Binary search the smallest speed k whose total hours sum(ceil(p / k)) fits in h.
from typing import List, Optional, Any


def minEatingSpeed(piles: List[int], h: int) -> int:
    def hours(k: int) -> int:
        return sum((p + k - 1) // k for p in piles)

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if hours(mid) <= h:
            hi = mid
        else:
            lo = mid + 1
    return lo
