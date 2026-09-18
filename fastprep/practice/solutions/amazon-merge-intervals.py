# Sort intervals by start, then sweep and extend the last merged interval when it overlaps.
from typing import List, Optional, Any


def solve(intervals: List[List[int]]) -> List[List[int]]:
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda iv: (iv[0], iv[1]))
    merged: List[List[int]] = []
    for start, end in ordered:
        if merged and start <= merged[-1][1]:
            if end > merged[-1][1]:
                merged[-1][1] = end
        else:
            merged.append([start, end])
    return merged
