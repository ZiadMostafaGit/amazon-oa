# Lazy k-way merge with a min-heap of (value, iterator index, position) holding one entry per live iterator.
from typing import List, Optional, Any
import heapq


def runUnionIterator(sortedIterators: List[List[int]], operations: List[str]) -> List[str]:
    heap = []
    for i, row in enumerate(sortedIterators):
        if row:
            heap.append((row[0], i, 0))
    heapq.heapify(heap)

    out = []
    for op in operations:
        if op == "has_next":
            out.append("true" if heap else "false")
        else:
            if not heap:
                out.append("ERROR_EXHAUSTED")
                continue
            val, i, pos = heapq.heappop(heap)
            out.append(str(val))
            nxt = pos + 1
            row = sortedIterators[i]
            if nxt < len(row):
                heapq.heappush(heap, (row[nxt], i, nxt))
    return out
