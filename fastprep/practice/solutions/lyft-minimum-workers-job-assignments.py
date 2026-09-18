# Sweep jobs by start time with a heap of busy end-times plus a min-heap of free worker IDs.
from typing import List, Optional, Any
import heapq


def assignWorkers(jobs: List[List[int]]) -> List[int]:
    n = len(jobs)
    if n == 0:
        return [0]
    order = sorted(range(n), key=lambda i: (
        (jobs[i][0] // 100) * 60 + jobs[i][0] % 100, i))
    assign = [0] * n
    busy = []          # (end_minute, worker_id)
    free = []          # available worker ids
    total = 0
    for i in order:
        hhmm, dur = jobs[i]
        start = (hhmm // 100) * 60 + hhmm % 100
        end = start + dur
        while busy and busy[0][0] <= start:
            _, wid = heapq.heappop(busy)
            heapq.heappush(free, wid)
        if free:
            wid = heapq.heappop(free)
        else:
            total += 1
            wid = total
        assign[i] = wid
        heapq.heappush(busy, (end, wid))
    return [total] + assign
