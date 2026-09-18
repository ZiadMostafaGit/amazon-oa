# Sweep line over +1 start / -1 (end+1) events sorted by time.
from typing import List, Optional, Any


def maximumConcurrentProcesses(processLogs: List[List[int]]) -> int:
    events = []
    for start, end in processLogs:
        events.append((start, 1))
        events.append((end + 1, -1))
    events.sort()
    best = 0
    cur = 0
    for _, delta in events:
        cur += delta
        if cur > best:
            best = cur
    return best
