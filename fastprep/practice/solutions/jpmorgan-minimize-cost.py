# Huffman-style greedy: repeatedly merge the two smallest values using a min-heap.
from typing import List, Optional, Any
import heapq


def minimizeCost(arr: List[int]) -> int:
    heap = list(arr)
    heapq.heapify(heap)
    total = 0
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        s = a + b
        total += s
        heapq.heappush(heap, s)
    return total
