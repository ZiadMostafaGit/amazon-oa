# Binary search the capability c; for a fixed c, greedily take every allowed value (<= c)
# whose left neighbour was not taken. Taking the earliest possible is never worse.
from typing import List, Optional, Any


def minimumSelectionCapability(values: List[int], count: int) -> int:
    def enough(c: int) -> bool:
        taken, i, n = 0, 0, len(values)
        while i < n:
            if values[i] <= c:
                taken += 1
                if taken >= count:
                    return True
                i += 2
            else:
                i += 1
        return taken >= count

    lo, hi = min(values), max(values)
    while lo < hi:
        mid = (lo + hi) // 2
        if enough(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
