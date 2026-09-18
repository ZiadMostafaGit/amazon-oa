# Greedy: sort projects by capital, push affordable profits into a max-heap, take the best k times.
import heapq
from typing import List, Optional, Any


def findMaximizedCapital(k: int, w: int, profits: List[int], capital: List[int]) -> int:
    n = len(profits)
    order = sorted(range(n), key=lambda i: capital[i])
    heap: List[int] = []
    idx = 0
    for _ in range(k):
        while idx < n and capital[order[idx]] <= w:
            heapq.heappush(heap, -profits[order[idx]])
            idx += 1
        if not heap:
            break
        w += -heapq.heappop(heap)
    return w
