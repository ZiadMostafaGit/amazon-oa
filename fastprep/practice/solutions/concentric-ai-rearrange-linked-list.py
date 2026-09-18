# Split at the middle, reverse the second half, then weave the two halves together.
from typing import Optional


def rearrangeList(head: Optional[ListNode]) -> Optional[ListNode]:
    if head is None or head.next is None:
        return head
    # find middle (slow ends at end of first half)
    slow, fast = head, head.next
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    second = slow.next
    slow.next = None
    # reverse second half
    prev = None
    while second is not None:
        nxt = second.next
        second.next = prev
        prev = second
        second = nxt
    # weave
    first = head
    while prev is not None:
        f_next = first.next
        p_next = prev.next
        first.next = prev
        prev.next = f_next
        first = f_next
        prev = p_next
    return head
