# Min-heap of size k (quickselect alternative) to find the kth largest occurrence.
import heapq
from typing import List, Optional, Any


def findKthLargest(nums: List[int], k: int) -> int:
    heap: List[int] = []
    for v in nums:
        if len(heap) < k:
            heapq.heappush(heap, v)
        elif v > heap[0]:
            heapq.heapreplace(heap, v)
    return heap[0]
