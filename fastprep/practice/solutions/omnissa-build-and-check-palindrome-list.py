# Build a singly linked list, then fast/slow pointers + in-place reversal of the second half.
from typing import List, Optional, Any


class _Node:
    __slots__ = ('val', 'next')

    def __init__(self, val: int):
        self.val = val
        self.next = None


def isPalindrome(values: List[int]) -> bool:
    head = None
    tail = None
    for v in values:
        node = _Node(v)
        if head is None:
            head = node
            tail = node
        else:
            tail.next = node
            tail = node

    if head is None or head.next is None:
        return True

    # locate middle
    slow = head
    fast = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next
        fast = fast.next.next

    # reverse second half starting after slow
    prev = None
    cur = slow.next
    while cur is not None:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt

    a = head
    b = prev
    ok = True
    while b is not None:
        if a.val != b.val:
            ok = False
            break
        a = a.next
        b = b.next
    return ok
