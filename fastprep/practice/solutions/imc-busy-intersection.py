# Event simulation with one FIFO queue per direction, jumping idle seconds forward.
from typing import List, Optional, Any
from collections import deque


def getResult(arrival: List[int], direction: List[int]) -> List[int]:
    n = len(arrival)
    res = [0] * n
    q = [deque(), deque()]
    i = 0
    t = 0
    prev = -1  # direction that crossed in the previous second, -1 if that second was idle
    while i < n or q[0] or q[1]:
        if not q[0] and not q[1] and arrival[i] > t:
            # the seconds between t and the next arrival are idle
            t = arrival[i]
            prev = -1
        while i < n and arrival[i] <= t:
            q[direction[i]].append(i)
            i += 1
        if q[0] and q[1]:
            d = 1 if prev == -1 else prev
        elif q[0]:
            d = 0
        else:
            d = 1
        car = q[d].popleft()
        res[car] = t
        prev = d
        t += 1
    return res
