# Simulation with a doubly linked list plus a lazy-deletion min-heap keyed by (value, index).
from typing import List, Optional, Any
import heapq


def selectLeastResourceTasks(resourceConsumption: List[int]) -> int:
    n = len(resourceConsumption)
    if n == 0:
        return 0
    prev = [i - 1 for i in range(n)]
    nxt = [i + 1 for i in range(n)]
    alive = [True] * n
    heap = [(v, i) for i, v in enumerate(resourceConsumption)]
    heapq.heapify(heap)

    def unlink(i: int) -> None:
        alive[i] = False
        p, q = prev[i], nxt[i]
        if p >= 0:
            nxt[p] = q
        if q < n:
            prev[q] = p

    total = 0
    while heap:
        v, i = heapq.heappop(heap)
        if not alive[i]:
            continue
        total += v
        left, right = prev[i], nxt[i]
        unlink(i)
        if left >= 0 and alive[left]:
            unlink(left)
        if right < n and alive[right]:
            unlink(right)
    return total
