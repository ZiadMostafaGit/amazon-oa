# Binary search the largest length L with sum(r // L) >= k.
from typing import List, Optional, Any


def maxLength(ribbons: List[int], k: int) -> int:
    lo, hi = 1, max(ribbons)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if sum(r // mid for r in ribbons) >= k:
            lo = mid
        else:
            hi = mid - 1
    return lo
