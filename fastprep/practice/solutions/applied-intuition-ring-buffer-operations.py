# Simulate a circular array with head index and size, wrapping both ends modulo capacity.
from typing import List, Optional, Any


def processRingBuffer(capacity: int, operations: List[str], values: List[int]) -> List[int]:
    buf = [0] * capacity
    head = 0
    size = 0
    out = []
    for i, op in enumerate(operations):
        if op == "push":
            if size < capacity:
                buf[(head + size) % capacity] = values[i]
                size += 1
                out.append(1)
            else:
                out.append(0)
        elif op == "pop":
            if size:
                out.append(buf[head])
                head = (head + 1) % capacity
                size -= 1
            else:
                out.append(-1)
        elif op == "front":
            out.append(buf[head] if size else -1)
        else:  # size
            out.append(size)
    return out
