# Sweep line over interval start/end+1 events, tracking the first coordinate reaching max coverage.
from typing import List, Optional, Any


def smallestMaximumOverlapPoint(intervals: List[List[int]]) -> int:
    events = []
    for lo, hi in intervals:
        events.append((lo, 1))
        events.append((hi + 1, -1))
    events.sort()

    best_count = 0
    best_point = intervals[0][0]
    count = 0
    i = 0
    n = len(events)
    while i < n:
        coord = events[i][0]
        while i < n and events[i][0] == coord:
            count += events[i][1]
            i += 1
        if count > best_count:
            best_count = count
            best_point = coord
    return best_point
