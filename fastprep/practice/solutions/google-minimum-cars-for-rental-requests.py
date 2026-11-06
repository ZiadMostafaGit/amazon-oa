from typing import List, Optional, Any
import heapq


def solve(requests: List[List[int]]) -> List[str]:
    order = sorted(requests, key=lambda r: (r[1], r[2], r[0]))
    free = []   # ids of cars available now (smallest id first)
    busy = []   # (return_time, car_id)
    cars = []   # per car id, record ids in assignment order
    for rid, pickup, ret in order:
        if ret <= pickup:  # empty interval: goes to car 0, availability unchanged
            if not cars:
                cars.append([])
                heapq.heappush(free, 0)
            cars[0].append(rid)
            continue
        while busy and busy[0][0] <= pickup:
            heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            car = heapq.heappop(free)
        else:
            car = len(cars)
            cars.append([])
        cars[car].append(rid)
        heapq.heappush(busy, (ret, car))
    return ["%d: %s" % (c, " ".join(map(str, ids))) for c, ids in enumerate(cars)]
