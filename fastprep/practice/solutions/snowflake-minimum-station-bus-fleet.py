# Greedy by departure time with a per-station min-heap of idle-bus availability times.
import heapq
from typing import List, Optional, Any


def minimumBuses(trips: List[List[str]]) -> int:
    parsed = []
    for t in trips:
        parsed.append((int(t[2]), int(t[3]), t[0], t[1]))
    parsed.sort(key=lambda r: (r[0], r[1]))

    idle = {}  # station -> min-heap of times at which a bus became free there
    buses = 0
    for dep, arr, origin, dest in parsed:
        heap = idle.get(origin)
        if heap and heap[0] <= dep:
            heapq.heappop(heap)
        else:
            buses += 1
        dheap = idle.get(dest)
        if dheap is None:
            dheap = []
            idle[dest] = dheap
        heapq.heappush(dheap, arr)
    return buses
