# Greedy with a max-heap: each operation halves the current largest element.
from typing import List, Optional, Any
import heapq


def minimumSumAfterHalves(values: List[int], k: int) -> int:
    total = sum(values)
    heap = [-v for v in values if v > 0]
    heapq.heapify(heap)
    for _ in range(k):
        if not heap:
            break
        top = -heap[0]
        reduced = -(-top // 2)  # ceil(top / 2)
        total -= top - reduced
        if reduced > 0:
            heapq.heapreplace(heap, -reduced)
        else:
            heapq.heappop(heap)
    return total
