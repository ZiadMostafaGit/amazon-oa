# Event simulation: process requests in arrival order, releasing finished servers from a
# min-heap by free time into a min-heap of available indices, then take the smallest index.
import heapq
from typing import List, Optional, Any


def getServerIndex(n: int, arrival: List[int], burstTime: List[int]) -> List[int]:
    m = len(arrival)
    order = sorted(range(m), key=lambda i: (arrival[i], i))
    available = list(range(1, n + 1))
    heapq.heapify(available)
    busy = []  # (free_time, server_index)
    res = []
    for i in order:
        t = arrival[i]
        while busy and busy[0][0] <= t:
            _, idx = heapq.heappop(busy)
            heapq.heappush(available, idx)
        if available:
            idx = heapq.heappop(available)
            heapq.heappush(busy, (t + burstTime[i], idx))
            res.append(idx)
        else:
            res.append(-1)
    return res
