# Slow/fast two-pointer walk; fast moves two steps so slow lands on the second middle.
from typing import Optional, Any


def middleNode(head: Optional[ListNode]) -> Optional[ListNode]:
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow
