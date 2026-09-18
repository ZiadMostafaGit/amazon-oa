# Sweep line over sorted arrival/departure times (half-open intervals).
from typing import List, Optional, Any


def minChairs(S: List[int], E: List[int]) -> int:
    starts = sorted(S)
    ends = sorted(E)
    n = len(starts)
    i = j = 0
    cur = best = 0
    while i < n:
        if starts[i] < ends[j]:
            cur += 1
            if cur > best:
                best = cur
            i += 1
        else:
            cur -= 1
            j += 1
    return best
