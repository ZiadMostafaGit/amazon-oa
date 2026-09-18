# Binary search for the first true in a monotone boolean array.
from typing import List, Optional, Any


def firstBadVersion(bad: List[bool]) -> int:
    lo, hi = 0, len(bad) - 1
    ans = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if bad[mid]:
            ans = mid
            hi = mid - 1
        else:
            lo = mid + 1
    return ans
