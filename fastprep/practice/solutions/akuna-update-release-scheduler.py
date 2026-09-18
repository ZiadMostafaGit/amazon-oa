# Greedy: process updates in planned-date order, taking the earliest option not before the last release.
from typing import List, Optional, Any


def minimumDays(n: int, plannedDate: List[int], alternateDate: List[int]) -> int:
    order = sorted(range(n), key=lambda i: plannedDate[i])
    last = 0
    for i in order:
        a, p = alternateDate[i], plannedDate[i]
        lo, hi = (a, p) if a <= p else (p, a)
        if lo >= last:
            day = lo
        elif hi >= last:
            day = hi
        else:
            day = hi
        if day > last:
            last = day
    return last
