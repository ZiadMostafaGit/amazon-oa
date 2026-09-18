# For each hub interval, count intersecting intervals via binary search on sorted starts and ends.
from typing import List, Optional, Any
import bisect


def minimumRetailers(zoneStart: List[int], zoneEnd: List[int]) -> int:
    n = len(zoneStart)
    if n == 0:
        return 0
    sortedStarts = sorted(zoneStart)
    sortedEnds = sorted(zoneEnd)

    best = 0
    for i in range(n):
        s = zoneStart[i]
        e = zoneEnd[i]
        # intervals whose start is strictly after e cannot intersect
        startsAfter = n - bisect.bisect_right(sortedStarts, e)
        # intervals whose end is strictly before s cannot intersect
        endsBefore = bisect.bisect_left(sortedEnds, s)
        count = n - startsAfter - endsBefore
        if count > best:
            best = count
    return n - best
