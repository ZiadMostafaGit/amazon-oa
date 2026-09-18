# Merge k sorted lists with a min-heap keyed on (value, list index).
from typing import List, Optional, Any
import heapq


def solve(lists: List[Optional['ListNode']]) -> Optional['ListNode']:
    heap = []
    for i, node in enumerate(lists or []):
        if node is not None:
            heapq.heappush(heap, (node.val, i, node))
    dummy = None
    tail = None
    while heap:
        val, i, node = heapq.heappop(heap)
        if tail is None:
            dummy = node
            tail = node
        else:
            tail.next = node
            tail = node
        nxt = node.next
        node.next = None
        if nxt is not None:
            heapq.heappush(heap, (nxt.val, i, nxt))
    return dummy
