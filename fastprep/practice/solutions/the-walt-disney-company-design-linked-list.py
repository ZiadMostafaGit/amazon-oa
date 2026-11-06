from typing import List, Optional, Any


class _Node:
    __slots__ = ("val", "next")

    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt


def runLinkedList(operations: List[List[int]]) -> List[int]:
    dummy = _Node(0)
    size = 0
    out = []

    def node_before(i):
        cur = dummy
        for _ in range(i):
            cur = cur.next
        return cur

    for kind, idx, val in operations:
        if kind == 0:
            if 0 <= idx < size:
                out.append(node_before(idx + 1).val)
            else:
                out.append(-1)
            continue
        if kind == 1:
            idx = 0
        elif kind == 2:
            idx = size
        if kind in (1, 2, 3):
            if idx < 0:
                idx = 0
            if idx <= size:
                p = node_before(idx)
                p.next = _Node(val, p.next)
                size += 1
        elif kind == 4:
            if 0 <= idx < size:
                p = node_before(idx)
                p.next = p.next.next
                size -= 1
        out.append(0)
    return out
