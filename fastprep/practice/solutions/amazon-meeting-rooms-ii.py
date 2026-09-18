# Sweep line over start/end events (+1 on start, -1 on end) tracking the peak overlap.
from typing import List, Optional, Any


def minMeetingRooms(intervals: List[List[int]]) -> int:
    events = []
    for interval in intervals:
        start, end = interval[0], interval[1]
        events.append((start, 1))
        events.append((end, -1))
    events.sort()
    current = 0
    best = 0
    for _, delta in events:
        current += delta
        if current > best:
            best = current
    return best
