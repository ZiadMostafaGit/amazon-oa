from typing import Optional, Any


def groupThirdNodes(head: Optional["ListNode"]) -> Optional["ListNode"]:
    keep_head = keep_tail = None
    third_head = third_tail = None
    pos = 1
    cur = head
    while cur:
        nxt = cur.next
        cur.next = None
        if pos % 3 == 0:
            if third_tail:
                third_tail.next = cur
            else:
                third_head = cur
            third_tail = cur
        else:
            if keep_tail:
                keep_tail.next = cur
            else:
                keep_head = cur
            keep_tail = cur
        pos += 1
        cur = nxt
    if keep_tail:
        keep_tail.next = third_head
        return keep_head
    return third_head
