# Sort by start, then sweep merging while next.start <= current.end (touching counts as overlap).
from typing import List, Optional, Any


def mergeIntervals(intervals: List[List[int]]) -> List[List[int]]:
    if not intervals:
        return []
    ordered = sorted((list(iv) for iv in intervals), key=lambda iv: (iv[0], iv[1]))
    merged = [[ordered[0][0], ordered[0][1]]]
    for start, end in ordered[1:]:
        last = merged[-1]
        if start <= last[1]:
            if end > last[1]:
                last[1] = end
        else:
            merged.append([start, end])
    return merged
