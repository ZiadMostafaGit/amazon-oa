# Two pointers with a tail pointer: always link the smaller head, then attach the leftover. O(n+m).
from typing import Optional, Any


def mergeTwoLists(list1: Optional["ListNode"], list2: Optional["ListNode"]) -> Optional["ListNode"]:
    head = tail = None
    a, b = list1, list2
    while a and b:
        if a.val <= b.val:
            node, a = a, a.next
        else:
            node, b = b, b.next
        if tail is None:
            head = tail = node
        else:
            tail.next = node
            tail = node
    rest = a if a else b
    if tail is None:
        return rest
    tail.next = rest
    return head
