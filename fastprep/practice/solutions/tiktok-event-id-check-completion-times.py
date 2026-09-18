# Single-server queue simulation: drain the waiting line up to each arrival, then admit or turn away.
from typing import List, Optional, Any
from collections import deque

CHECK = 300  # 5 minutes in seconds
CAPACITY = 10


def solution(times: List[int]) -> List[int]:
    n = len(times)
    res = [0] * n
    order = sorted(range(n), key=lambda i: times[i])
    queue = deque()
    free = 0  # time at which the ID checker becomes available

    for i in order:
        t = times[i]
        # Serve everyone whose check can begin at or before this arrival moment.
        while queue and free <= t:
            a, j = queue.popleft()
            start = free if free > a else a
            free = start + CHECK
            res[j] = free
        if len(queue) > CAPACITY:
            res[i] = t  # leaves immediately
        else:
            queue.append((t, i))

    while queue:
        a, j = queue.popleft()
        start = free if free > a else a
        free = start + CHECK
        res[j] = free

    return res
