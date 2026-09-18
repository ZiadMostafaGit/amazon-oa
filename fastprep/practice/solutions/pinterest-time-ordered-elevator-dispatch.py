# Direct time-stepped simulation: advance moving elevators, pick nearest eligible one per request.
from typing import List, Optional, Any


def dispatchFinalPassenger(elevatorFloors: List[int], requestFloors: List[int], requestDirections: List[int], requestTimes: List[int]) -> int:
    n = len(elevatorFloors)
    floors = list(elevatorFloors)
    dirs = [0] * n           # 0 = idle, 1 = up, -1 = down
    prev_time = requestTimes[0] if requestTimes else 0
    result = -1
    for i in range(len(requestFloors)):
        t = requestTimes[i]
        dt = t - prev_time
        prev_time = t
        if dt:
            for j in range(n):
                if dirs[j]:
                    floors[j] += dirs[j] * dt
        pf = requestFloors[i]
        pd = requestDirections[i]
        best = -1
        best_dist = None
        for j in range(n):
            d = dirs[j]
            if d == 0:
                eligible = True
            elif d == 1:
                eligible = (pd == 1 and pf >= floors[j])
            else:
                eligible = (pd == -1 and pf <= floors[j])
            if not eligible:
                continue
            dist = abs(pf - floors[j])
            if best_dist is None or dist < best_dist:
                best_dist = dist
                best = j
        if best != -1:
            floors[best] = pf
            dirs[best] = pd
        result = best
    return result
