# Binary search the sorted pings to mark five 60-second slots active, then scan for three consecutive empty slots.
from typing import List, Optional, Any
import bisect


def wasAlive(pingTimestamps: List[int], queryTime: int) -> bool:
    active = []
    for k in range(5):
        lo = queryTime + 60 * k
        hi = lo + 60
        i = bisect.bisect_left(pingTimestamps, lo)
        active.append(i < len(pingTimestamps) and pingTimestamps[i] < hi)
    run = 0
    for a in active:
        if a:
            run = 0
        else:
            run += 1
            if run >= 3:
                return False
    return True
