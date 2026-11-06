# Drive as far as fuel allows; when stuck, retroactively take the biggest station passed (max-heap).
from typing import List, Optional, Any
import heapq


def minRefuelStops(target: int, startFuel: int, stations: List[List[int]]) -> int:
    st = sorted(stations)
    heap = []
    fuel = startFuel
    stops = 0
    i = 0
    while fuel < target:
        while i < len(st) and st[i][0] <= fuel:
            heapq.heappush(heap, -st[i][1])
            i += 1
        if not heap:
            return -1
        fuel += -heapq.heappop(heap)
        stops += 1
    return stops
