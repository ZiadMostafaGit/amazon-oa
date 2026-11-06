# Three phases over the sorted list: copy intervals ending before the new one, absorb overlaps, copy the rest.
from typing import List, Optional, Any


def insertInterval(intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
    res = []
    s, e = newInterval
    i, n = 0, len(intervals)
    while i < n and intervals[i][1] < s:
        res.append(list(intervals[i]))
        i += 1
    while i < n and intervals[i][0] <= e:
        s = min(s, intervals[i][0])
        e = max(e, intervals[i][1])
        i += 1
    res.append([s, e])
    while i < n:
        res.append(list(intervals[i]))
        i += 1
    return res
