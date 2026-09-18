# Greedy with a min-heap: repeatedly merge the two shortest ropes (Huffman).
import heapq
from typing import List, Optional, Any


def minimumRopeConnectionCost(ropes: List[int]) -> int:
    if len(ropes) <= 1:
        return 0
    heap = list(ropes)
    heapq.heapify(heap)
    total = 0
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        s = a + b
        total += s
        heapq.heappush(heap, s)
    return total
