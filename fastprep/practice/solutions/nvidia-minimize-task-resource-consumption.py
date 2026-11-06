from typing import List, Optional, Any
import heapq


def minimizeTaskResourceConsumption(resourceConsumption: List[int]) -> int:
    a = resourceConsumption
    n = len(a)
    prv = list(range(-1, n - 1))
    nxt = list(range(1, n + 1))
    alive = [True] * n
    heap = [(v, i) for i, v in enumerate(a)]  # current order = original order among survivors
    heapq.heapify(heap)

    def remove(i):
        alive[i] = False
        p, q = prv[i], nxt[i]
        if p >= 0:
            nxt[p] = q
        if q < n:
            prv[q] = p

    total = 0
    while heap:
        v, i = heapq.heappop(heap)
        if not alive[i]:
            continue
        total += v
        p, q = prv[i], nxt[i]
        remove(i)
        if p >= 0:
            remove(p)
        if q < n:
            remove(q)
    return total
