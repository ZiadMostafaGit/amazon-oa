# Approach: digit-array schoolbook subtraction with borrow, right-to-left, then strip leading zeros.
from typing import Optional, Any, List


def _digits(node: Optional[ListNode]) -> List[int]:
    out = []
    while node is not None:
        out.append(node.val)
        node = node.next
    return out


def subtractForwardOrder(minuend: Optional[ListNode], subtrahend: Optional[ListNode]) -> Optional[ListNode]:
    a = _digits(minuend)
    b = _digits(subtrahend)
    res = []
    borrow = 0
    i, j = len(a) - 1, len(b) - 1
    while i >= 0:
        d = a[i] - borrow - (b[j] if j >= 0 else 0)
        if d < 0:
            d += 10
            borrow = 1
        else:
            borrow = 0
        res.append(d)
        i -= 1
        j -= 1
    res.reverse()
    k = 0
    while k < len(res) - 1 and res[k] == 0:
        k += 1
    res = res[k:]
    head = None
    tail = None
    for d in res:
        node = ListNode(d)
        if head is None:
            head = node
        else:
            tail.next = node
        tail = node
    return head
