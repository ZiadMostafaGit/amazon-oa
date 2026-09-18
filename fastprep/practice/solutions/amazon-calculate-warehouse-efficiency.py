# Approach: each parcel has a deadline min(i, n-1-i)+1; classic deadline scheduling
# greedy with a min-heap keeping the best feasible set of one pick per day.
from typing import List, Optional, Any
import heapq


def calculateWarehouseEfficiency(parcelWeights: List[int]) -> int:
    n = len(parcelWeights)
    items = []
    for i, w in enumerate(parcelWeights):
        items.append((min(i, n - 1 - i) + 1, w))
    items.sort(key=lambda x: x[0])
    heap = []
    for deadline, w in items:
        heapq.heappush(heap, w)
        if len(heap) > deadline:
            heapq.heappop(heap)
    return sum(heap)
