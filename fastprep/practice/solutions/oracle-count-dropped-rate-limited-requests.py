# Sliding-window (two-pointer) counting: every request, dropped or not, occupies window capacity.
from typing import List, Optional, Any


def countDroppedRequests(requestTimes: List[int]) -> int:
    n = len(requestTimes)
    dropped = 0
    lo1 = 0   # start of same-second window
    lo10 = 0  # start of [t-9, t]
    lo60 = 0  # start of [t-59, t]
    for i in range(n):
        t = requestTimes[i]
        while requestTimes[lo1] < t:
            lo1 += 1
        while requestTimes[lo10] < t - 9:
            lo10 += 1
        while requestTimes[lo60] < t - 59:
            lo60 += 1
        if (i - lo1 + 1) > 3 or (i - lo10 + 1) > 20 or (i - lo60 + 1) > 60:
            dropped += 1
    return dropped
