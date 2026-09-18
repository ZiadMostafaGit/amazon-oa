# Approach: sweep line over sorted start and end times, tracking the peak concurrency.
from typing import List, Optional, Any


def minMeetingRooms(meetingTimings: List[List[int]]) -> int:
    starts = sorted(m[0] for m in meetingTimings)
    ends = sorted(m[1] for m in meetingTimings)
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
