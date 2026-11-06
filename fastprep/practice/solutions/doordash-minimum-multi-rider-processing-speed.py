# Binary search the speed k; for a fixed k, greedily give each rider as many consecutive
# orders as fit in hoursPerRider and count riders used.
from typing import List, Optional, Any


def minimumMultiRiderSpeed(workloads: List[int], riders: int, hoursPerRider: int) -> int:
    def ridersNeeded(k: int) -> int:
        used, left = 1, hoursPerRider
        for w in workloads:
            h = (w + k - 1) // k
            if h > hoursPerRider:
                return riders + 1
            if h > left:
                used += 1
                left = hoursPerRider
                if used > riders:
                    return used
            left -= h
        return used

    lo, hi = 1, max(workloads)
    while lo < hi:
        mid = (lo + hi) // 2
        if ridersNeeded(mid) <= riders:
            hi = mid
        else:
            lo = mid + 1
    return lo
