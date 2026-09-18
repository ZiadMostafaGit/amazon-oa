# Two heaps (max-heap of the lower half, min-heap of the upper half) giving the lower median.
from typing import List, Optional, Any
import heapq


def solve(deliveryTimes: List[int]) -> List[int]:
    low = []   # max-heap (negated) holding the smaller half, its top is the lower median
    high = []  # min-heap holding the larger half
    out = []

    for x in deliveryTimes:
        if low and x > -low[0]:
            heapq.heappush(high, x)
        else:
            heapq.heappush(low, -x)

        # keep len(low) == len(high) or len(low) == len(high) + 1
        if len(low) > len(high) + 1:
            heapq.heappush(high, -heapq.heappop(low))
        elif len(high) > len(low):
            heapq.heappush(low, -heapq.heappop(high))

        out.append(-low[0])

    return out
