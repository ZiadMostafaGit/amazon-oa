# Single-server queue simulation: drain finished checks at each arrival, then admit or turn away.
from collections import deque
from typing import List, Optional, Any

CHECK = 300
CAPACITY = 10


def solution(times: List[int]) -> List[int]:
    n = len(times)
    res = [0] * n
    queue = deque()
    free_time = 0 if n == 0 else times[0]
    for i, t in enumerate(times):
        # completions that happen at or before this arrival start the next waiting person
        while queue and free_time <= t:
            head = queue.popleft()
            free_time += CHECK
            res[head] = free_time
        if not queue and free_time < t:
            free_time = t
        if len(queue) > CAPACITY:
            res[i] = t
        else:
            queue.append(i)
    while queue:
        head = queue.popleft()
        free_time += CHECK
        res[head] = free_time
    return res
