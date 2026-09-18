# Sweep requests by pickup time; free cars go into a min-heap by id, busy cars into a heap by return time.
from typing import List, Optional, Any
import heapq


def assignMinimumCars(requests: List[List[int]]) -> List[str]:
    order = sorted(requests, key=lambda r: (r[0], r[1]))
    free = []   # car ids available now
    busy = []   # (return_time, car_id)
    assignment = []  # per car id, list of (pickup, ret)
    for pickup, ret in order:
        while busy and busy[0][0] <= pickup:
            heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            car = heapq.heappop(free)
        else:
            car = len(assignment)
            assignment.append([])
        assignment[car].append((pickup, ret))
        heapq.heappush(busy, (ret, car))
    return [
        "%d: %s" % (car, " ".join("(%d,%d)" % pair for pair in items))
        for car, items in enumerate(assignment)
    ]
