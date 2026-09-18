# Greedy with a max-heap: always halve the current largest value, since that removes the most.
from typing import List, Optional, Any
import heapq


def minimumHalvingOperations(values: List[int]) -> int:
    original = sum(values)
    current = original
    heap = [-v for v in values]
    heapq.heapify(heap)
    ops = 0
    while 2 * current > original:
        top = -heap[0]
        if top == 0:
            break
        nxt = top // 2
        heapq.heapreplace(heap, -nxt)
        current -= top - nxt
        ops += 1
    return ops
