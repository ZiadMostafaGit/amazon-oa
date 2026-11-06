# Count, then keep a min-heap of size k keyed by (frequency, -value): the root is the weakest of the current top k.
import heapq
from collections import Counter
from typing import List, Optional, Any


def solveTopKFrequentElements(nums: List[int], k: int) -> List[int]:
    heap = []
    for v, f in Counter(nums).items():
        item = (f, -v)
        if len(heap) < k:
            heapq.heappush(heap, item)
        elif item > heap[0]:
            heapq.heapreplace(heap, item)
    heap.sort(reverse=True)
    return [-nv for _, nv in heap]
