# Binary search the largest gap d such that greedily placing cows (leftmost first) fits k of them.
from typing import List, Optional, Any


def maximumMinimumDistance(stalls: List[int], k: int) -> int:
    s = sorted(stalls)

    def fits(d: int) -> bool:
        placed, last = 1, s[0]
        for x in s[1:]:
            if x - last >= d:
                placed += 1
                last = x
                if placed >= k:
                    return True
        return placed >= k

    lo, hi = 1, s[-1] - s[0]
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if fits(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo
