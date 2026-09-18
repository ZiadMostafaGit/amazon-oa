# Greedy activity selection: sort by end, keep intervals that start at or after the last kept end.
from typing import List, Optional, Any


def minimumIntervalRemovals(intervals: List[List[int]]) -> int:
    if not intervals:
        return 0
    order = sorted(intervals, key=lambda iv: iv[1])
    kept = 0
    last_end = None
    for s, e in order:
        if last_end is None or s >= last_end:
            kept += 1
            last_end = e
    return len(intervals) - kept
