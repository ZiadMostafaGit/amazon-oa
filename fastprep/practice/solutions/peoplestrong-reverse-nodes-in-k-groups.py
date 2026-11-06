from typing import Optional, Any


def reverseKGroup(head: Optional["ListNode"], k: int) -> Optional["ListNode"]:
    new_head = None
    prev_tail = None      # last node of the already-processed part
    cur = head
    while cur:
        # check that a full group of k nodes starts here
        probe, cnt = cur, 0
        while probe and cnt < k:
            probe = probe.next
            cnt += 1
        if cnt < k:
            if prev_tail:
                prev_tail.next = cur
            else:
                new_head = cur
            break
        # reverse k nodes starting at cur; probe is the node after the group
        prev, node = probe, cur
        for _ in range(k):
            nxt = node.next
            node.next = prev
            prev, node = node, nxt
        if prev_tail:
            prev_tail.next = prev
        else:
            new_head = prev
        prev_tail = cur
        cur = probe
    return new_head
