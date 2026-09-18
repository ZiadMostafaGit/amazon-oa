# Approach: min-heap of size k holding the k largest values seen so far; its root is the kth largest.
from typing import List, Optional, Any
import heapq


def kthLargestAfterEachAdd(k: int, initialValues: List[int], additions: List[int]) -> List[int]:
    heap = list(initialValues)
    heapq.heapify(heap)
    while len(heap) > k:
        heapq.heappop(heap)
    out = []
    for value in additions:
        if len(heap) < k:
            heapq.heappush(heap, value)
        elif value > heap[0]:
            heapq.heapreplace(heap, value)
        out.append(heap[0])
    return out
