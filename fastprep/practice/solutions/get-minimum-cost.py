# Greedy with a min-heap: repeatedly buy the cheapest next unit a[i] + count[i]*b[i].
from typing import List, Optional, Any
import heapq


def getMinimumCost(a: List[int], b: List[int], m: int) -> int:
    n = len(a)
    heap = [(a[i], i) for i in range(n)]
    heapq.heapify(heap)
    total = 0
    for _ in range(m):
        cost, i = heapq.heappop(heap)
        total += cost
        heapq.heappush(heap, (cost + b[i], i))
    return total
