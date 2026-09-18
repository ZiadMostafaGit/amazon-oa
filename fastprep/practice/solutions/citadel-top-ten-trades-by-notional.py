# Bounded min-heap of size 10 keyed by (notional, -index) so the weakest candidate is evicted in O(log 10).
import heapq
from typing import List, Optional, Any


def topTenTrades(trades: List[List[str]]) -> List[str]:
    K = 10
    heap = []  # (notional, -index, tradeId)
    for i, row in enumerate(trades):
        notional = int(row[2]) * int(row[3])
        entry = (notional, -i, row[0])
        if len(heap) < K:
            heapq.heappush(heap, entry)
        elif entry > heap[0]:
            heapq.heapreplace(heap, entry)
    heap.sort(reverse=True)
    return [entry[2] for entry in heap]
