# Max-heap simulation: smash the two largest until at most one stone remains. O(n log n).
import heapq
from typing import List, Optional, Any


def lastStoneWeight(weights: List[int]) -> int:
    heap = [-w for w in weights]
    heapq.heapify(heap)
    while len(heap) > 1:
        a = -heapq.heappop(heap)
        b = -heapq.heappop(heap)
        if a != b:
            heapq.heappush(heap, -(a - b))
    return -heap[0] if heap else 0
