# Min-heap over the current head of each list, relinking nodes in place.
import heapq
from typing import List, Optional, Any


def mergeKLists(lists: List[Optional["ListNode"]]) -> Optional["ListNode"]:
    heap = []
    for idx, node in enumerate(lists or []):
        if node is not None:
            heapq.heappush(heap, (node.val, idx, node))
    dummy = None
    tail = None
    while heap:
        val, idx, node = heapq.heappop(heap)
        if tail is None:
            dummy = tail = node
        else:
            tail.next = node
            tail = node
        nxt = node.next
        node.next = None
        if nxt is not None:
            heapq.heappush(heap, (nxt.val, idx, nxt))
    return dummy
