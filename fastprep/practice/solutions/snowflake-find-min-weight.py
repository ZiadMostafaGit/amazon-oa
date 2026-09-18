# Greedy with a max-heap: each day halve the heaviest chocolate; stop early once every weight is 1.
import heapq
from typing import List, Optional, Any


def findMinWeight(weights: List[int], d: int) -> int:
    heap = [-w for w in weights]
    heapq.heapify(heap)
    total = sum(weights)
    for _ in range(d):
        top = -heap[0]
        eaten = top // 2
        if eaten == 0:
            break
        total -= eaten
        heapq.heapreplace(heap, -(top - eaten))
    return total
