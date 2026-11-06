from typing import List, Optional, Any
import heapq


def mergeKLists(lists: List[Optional["ListNode"]]) -> Optional["ListNode"]:
    heap = [(node.val, i, node) for i, node in enumerate(lists) if node]
    heapq.heapify(heap)
    head = tail = None
    while heap:
        _, i, node = heapq.heappop(heap)
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
        node.next = None
        if tail:
            tail.next = node
        else:
            head = node
        tail = node
    return head
