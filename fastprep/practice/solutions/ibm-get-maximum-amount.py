# Greedy with a max-heap: always sell from the type with the largest remaining count.
import heapq
from typing import List


def getMaximumAmount(quantity: List[int], m: int) -> int:
    heap = [-q for q in quantity if q > 0]
    heapq.heapify(heap)
    total = 0
    for _ in range(m):
        if not heap:
            break
        top = -heapq.heappop(heap)
        total += top
        if top - 1 > 0:
            heapq.heappush(heap, -(top - 1))
    return total
