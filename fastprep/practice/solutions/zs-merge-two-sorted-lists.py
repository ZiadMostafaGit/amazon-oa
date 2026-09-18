# Two-pointer splice of the existing nodes into one sorted list.
from typing import Optional, Any


def mergeTwoLists(listA: Optional[ListNode], listB: Optional[ListNode]) -> Optional[ListNode]:
    dummy = ListNode(0)
    tail = dummy
    a, b = listA, listB
    while a is not None and b is not None:
        if a.val <= b.val:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a if a is not None else b
    return dummy.next
