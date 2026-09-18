# Binary search on the answer capacity, greedily counting the days each candidate needs.
from typing import List, Optional, Any


def solve(weights: List[int], days: int) -> int:
    def needed(cap: int) -> int:
        d = 1
        cur = 0
        for w in weights:
            if cur + w > cap:
                d += 1
                cur = 0
            cur += w
        return d

    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if needed(mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo
