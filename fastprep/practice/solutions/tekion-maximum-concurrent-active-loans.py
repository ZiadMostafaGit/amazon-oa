# Sweep line over sorted start/end events (ends processed before starts at equal time).
from typing import List, Optional, Any


def maxActiveLoans(loans: List[List[int]]) -> int:
    events = []
    for start, end in loans:
        events.append((start, 1))
        events.append((end, -1))
    events.sort(key=lambda e: (e[0], e[1]))
    best = 0
    cur = 0
    for _, delta in events:
        cur += delta
        if cur > best:
            best = cur
    return best
