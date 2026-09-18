# Simulation over a hand-built singly linked list with explicit head/tail pointers.
from typing import List, Optional, Any


class _Node:
    __slots__ = ("val", "next")

    def __init__(self, val: int):
        self.val = val
        self.next = None


def processLinkedQueue(operations: List[str], values: List[int]) -> List[int]:
    head = None
    tail = None
    out: List[int] = []

    for op, v in zip(operations, values):
        if op == "enqueue":
            node = _Node(v)
            if head is None:
                head = node
                tail = node
            else:
                tail.next = node
                tail = node
        elif op == "dequeue":
            if head is None:
                continue
            out.append(head.val)
            head = head.next
            if head is None:
                tail = None
        elif op == "delete":
            prev = None
            cur = head
            while cur is not None and cur.val != v:
                prev = cur
                cur = cur.next
            if cur is not None:
                if prev is None:
                    head = cur.next
                else:
                    prev.next = cur.next
                if cur is tail:
                    tail = prev
                cur.next = None
        elif op == "removeAllDuplicates":
            seen = set()
            prev = None
            cur = head
            while cur is not None:
                nxt = cur.next
                if cur.val in seen:
                    if prev is None:
                        head = nxt
                    else:
                        prev.next = nxt
                    cur.next = None
                else:
                    seen.add(cur.val)
                    prev = cur
                cur = nxt
            tail = prev
    return out
