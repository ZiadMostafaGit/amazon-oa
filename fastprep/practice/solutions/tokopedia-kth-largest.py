# Quickselect-style: use heapq.nlargest / partial selection for O(n) average.
from typing import List, Optional, Any
import heapq


def findKthLargest(nums: List[int], k: int) -> int:
    h = []
    for v in nums:
        if len(h) < k:
            heapq.heappush(h, v)
        elif v > h[0]:
            heapq.heapreplace(h, v)
    return h[0]
