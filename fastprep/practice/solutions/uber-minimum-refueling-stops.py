# Greedy with a max-heap of passed stations' fuel; refuel from the largest whenever stuck.
from typing import List, Optional, Any
import heapq


def minRefuelStops(target: int, startFuel: int, stations: List[List[int]]) -> int:
    stations = sorted(stations, key=lambda s: s[0])
    heap = []  # max-heap via negated fuel
    fuel = startFuel
    stops = 0
    i = 0
    n = len(stations)
    while fuel < target:
        while i < n and stations[i][0] <= fuel:
            heapq.heappush(heap, -stations[i][1])
            i += 1
        if not heap:
            return -1
        fuel += -heapq.heappop(heap)
        stops += 1
    return stops
