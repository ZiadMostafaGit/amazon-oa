# Greedy with a max-heap: each voucher halves the currently most expensive item.
from typing import List, Optional, Any
import heapq


def getMinimumTotalCost(vouchersCount: int, prices: List[int]) -> int:
    heap = [-p for p in prices]
    heapq.heapify(heap)
    for _ in range(vouchersCount):
        if not heap:
            break
        top = -heap[0]
        if top == 0:
            break
        heapq.heapreplace(heap, -(top // 2))
    return -sum(heap)
