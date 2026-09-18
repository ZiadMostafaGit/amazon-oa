# Sweep line over sorted start and end times, tracking peak concurrent meetings.
from typing import List, Optional, Any


def minMeetingRooms(intervals: List[List[int]]) -> int:
    if not intervals:
        return 0
    starts = sorted(iv[0] for iv in intervals)
    ends = sorted(iv[1] for iv in intervals)
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
