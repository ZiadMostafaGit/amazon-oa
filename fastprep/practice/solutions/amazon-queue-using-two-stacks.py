from typing import List, Optional, Any


class _TwoStackQueue:
    """FIFO queue backed by exactly two LIFO stacks (amortized O(1) ops)."""

    def __init__(self):
        self.inbox = []
        self.outbox = []

    def push(self, x: int) -> None:
        self.inbox.append(x)

    def _shift(self) -> None:
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())

    def pop(self):
        self._shift()
        if not self.outbox:
            return None
        return self.outbox.pop()

    def peek(self):
        self._shift()
        if not self.outbox:
            return None
        return self.outbox[-1]

    def empty(self) -> bool:
        return not self.inbox and not self.outbox


def solve(operations: List[str], values: List[int]) -> List[str]:
    q = _TwoStackQueue()
    out = []
    for i, op in enumerate(operations):
        name = op.strip().lower()
        if name == "push":
            q.push(values[i])
        elif name == "pop":
            v = q.pop()
            out.append("-1" if v is None else str(v))
        elif name == "peek":
            v = q.peek()
            out.append("-1" if v is None else str(v))
        elif name == "empty":
            out.append("true" if q.empty() else "false")
    return out
