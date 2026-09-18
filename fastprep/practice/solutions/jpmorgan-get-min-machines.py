# Approach: sweep line over inclusive intervals (+1 at start, -1 just after end), track max concurrent tasks.
from typing import List, Optional, Any


def getMinMachines(start: List[int], end: List[int]) -> int:
    events = []
    for s, e in zip(start, end):
        events.append((s, 1))
        events.append((e + 1, -1))
    events.sort()
    cur = 0
    best = 0
    for _, d in events:
        cur += d
        if cur > best:
            best = cur
    return best
