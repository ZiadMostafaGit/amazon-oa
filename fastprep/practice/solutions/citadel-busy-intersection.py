# Event simulation with two FIFO queues, skipping idle gaps by jumping to the next arrival time.
from typing import List, Optional, Any
from collections import deque


def serviceTimes(arrivalTimes: List[int], directions: List[int]) -> List[int]:
    n = len(arrivalTimes)
    result = [0] * n
    queues = (deque(), deque())
    p = 0
    served = 0
    t = 0
    last_dir: Optional[int] = None
    while served < n:
        while p < n and arrivalTimes[p] <= t:
            queues[directions[p]].append(p)
            p += 1
        if not queues[0] and not queues[1]:
            t = arrivalTimes[p]
            last_dir = None
            continue
        if not queues[0]:
            d = 1
        elif not queues[1]:
            d = 0
        elif last_dir is not None:
            d = last_dir
        else:
            d = 1
        idx = queues[d].popleft()
        result[idx] = t
        served += 1
        last_dir = d
        t += 1
    return result
