# Two pointers n nodes apart: when the lead reaches the last node, the trailer sits just before the target.
from typing import Optional


def removeNthFromEnd(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    dummy = ListNode(0)
    dummy.next = head
    lead = trail = dummy
    for _ in range(n):
        lead = lead.next
    while lead.next:
        lead = lead.next
        trail = trail.next
    trail.next = trail.next.next
    return dummy.next
