from typing import Optional, Any


def rearrangeDivisible(head: Optional["ListNode"], divisor: int, k: int) -> Optional["ListNode"]:
    # 1. reverse the first k nodes in place
    if k > 0 and head:
        prev, cur = None, head
        for _ in range(k):
            nxt = cur.next
            cur.next = prev
            prev, cur = cur, nxt
        head.next = cur      # old head is now the k-th node
        head = prev
    # 2. split into two stable chains
    div_head = div_tail = None
    oth_head = oth_tail = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = None
        if cur.val % divisor == 0:
            if div_tail:
                div_tail.next = cur
            else:
                div_head = cur
            div_tail = cur
        else:
            if oth_tail:
                oth_tail.next = cur
            else:
                oth_head = cur
            oth_tail = cur
        cur = nxt
    # 3. weave them, starting with a divisible node
    a, b = div_head, oth_head
    new_head = tail = None
    take_a = True
    while a or b:
        if (take_a and a) or not b:
            node, a = a, a.next
        else:
            node, b = b, b.next
        node.next = None
        if tail:
            tail.next = node
        else:
            new_head = node
        tail = node
        take_a = not take_a
    return new_head
