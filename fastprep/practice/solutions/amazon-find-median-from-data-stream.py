# Two heaps (max-heap for lower half, min-heap for upper half) to track the running median.
import heapq
from typing import List, Optional, Any


def solve(operations: List[List[str]]) -> List[float]:
    low: List[int] = []   # max-heap via negation (lower half)
    high: List[int] = []  # min-heap (upper half)
    out: List[float] = []

    for row in operations:
        if not row:
            continue
        op = row[0]
        if len(row) >= 2 and op != "median":
            num = int(row[1])
            heapq.heappush(low, -num)
            heapq.heappush(high, -heapq.heappop(low))
            if len(high) > len(low):
                heapq.heappush(low, -heapq.heappop(high))
        else:
            if not low:
                continue
            if len(low) > len(high):
                out.append(float(-low[0]))
            else:
                out.append((-low[0] + high[0]) / 2.0)
    return out
