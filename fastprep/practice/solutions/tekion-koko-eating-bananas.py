# Binary search the eating speed; feasibility is the sum of ceil(pile/k) hours.
from typing import List, Optional, Any


def minEatingSpeed(piles: List[int], h: int) -> int:
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        hours = 0
        for p in piles:
            hours += (p + mid - 1) // mid
            if hours > h:
                break
        if hours <= h:
            hi = mid
        else:
            lo = mid + 1
    return lo
