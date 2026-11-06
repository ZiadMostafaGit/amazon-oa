# Iterative pointer reversal: walk once, flipping each next pointer. O(n) time, O(1) space.
from typing import Optional, Any


def reverseList(head: Optional["ListNode"]) -> Optional["ListNode"]:
    prev = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    return prev
