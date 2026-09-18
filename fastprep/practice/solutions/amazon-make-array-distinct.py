# Sweep values upward with a max-heap of costs: the priciest item keeps the current value, the rest pay one increment each.
import heapq
from typing import List, Optional, Any


def makeArrayDistinct(size: List[int], cost: List[int]) -> int:
    items = sorted(zip(size, cost))
    n = len(items)
    heap = []
    pending = 0  # sum of costs currently waiting in the heap
    total = 0
    i = 0
    v = items[0][0] if n else 0
    while i < n or heap:
        if not heap and i < n and items[i][0] > v:
            v = items[i][0]
        while i < n and items[i][0] == v:
            heapq.heappush(heap, -items[i][1])
            pending += items[i][1]
            i += 1
        if heap:
            top = -heapq.heappop(heap)
            pending -= top
        total += pending
        v += 1
    return total
