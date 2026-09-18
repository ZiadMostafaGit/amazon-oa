# Hand-rolled binary min-heap (array-based sift-up / sift-down), no heapq.
from typing import List, Optional, Any


class _MinHeap:
    def __init__(self) -> None:
        self.a: List[int] = []

    def push(self, v: int) -> None:
        a = self.a
        a.append(v)
        i = len(a) - 1
        while i > 0:
            p = (i - 1) >> 1
            if a[p] <= a[i]:
                break
            a[p], a[i] = a[i], a[p]
            i = p

    def peek(self) -> int:
        return self.a[0]

    def pop(self) -> int:
        a = self.a
        top = a[0]
        last = a.pop()
        if a:
            a[0] = last
            n = len(a)
            i = 0
            while True:
                l = 2 * i + 1
                r = l + 1
                s = i
                if l < n and a[l] < a[s]:
                    s = l
                if r < n and a[r] < a[s]:
                    s = r
                if s == i:
                    break
                a[i], a[s] = a[s], a[i]
                i = s
        return top


def runPriorityQueue(operations: List[str], values: List[int]) -> List[int]:
    h = _MinHeap()
    out: List[int] = []
    for i, op in enumerate(operations):
        if op == "PUSH":
            h.push(values[i])
        elif op == "PEEK":
            out.append(h.peek())
        else:
            out.append(h.pop())
    return out
