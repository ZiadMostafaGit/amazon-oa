# Min-heap of the climbs given ropes; when it overflows, pay the smallest climb with sandbags.
from typing import List, Optional, Any
import heapq


def furthestBuilding(heights: List[int], sandbags: int, ropes: int) -> int:
    heap = []
    for i in range(len(heights) - 1):
        d = heights[i + 1] - heights[i]
        if d <= 0:
            continue
        heapq.heappush(heap, d)
        if len(heap) > ropes:
            sandbags -= heapq.heappop(heap)
            if sandbags < 0:
                return i
    return len(heights) - 1
