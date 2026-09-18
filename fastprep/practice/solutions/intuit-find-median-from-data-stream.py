# Two heaps (max-heap for lower half, min-heap for upper half) to track the running median.
import heapq
from typing import List, Optional, Any


def processMedianOperations(operations: List[List[str]]) -> List[float]:
    low = []   # max-heap (negated) of the smaller half
    high = []  # min-heap of the larger half
    out: List[float] = []
    for op in operations:
        kind = op[0]
        if kind == "add":
            v = int(op[1])
            heapq.heappush(low, -v)
            heapq.heappush(high, -heapq.heappop(low))
            if len(high) > len(low):
                heapq.heappush(low, -heapq.heappop(high))
        else:
            if len(low) > len(high):
                out.append(float(-low[0]))
            else:
                out.append((-low[0] + high[0]) / 2.0)
    return out
