# Simulate a dynamic-array set: ordered list for storage plus a dict index for O(1) membership.
from typing import List, Optional, Any


def dynamicArraySet(operations: List[str], initialCapacity: int) -> List[str]:
    capacity = initialCapacity
    items: List[int] = []          # preserves insertion order of live values
    pos = {}                       # value -> index in items
    out: List[str] = []

    for op in operations:
        parts = op.split()
        cmd = parts[0].upper()

        if cmd == "SIZE":
            out.append(str(len(items)))
            continue
        if cmd == "CAPACITY":
            out.append(str(capacity))
            continue

        value = int(parts[1])

        if cmd == "CONTAINS":
            out.append("true" if value in pos else "false")
        elif cmd == "ADD":
            if value in pos:
                out.append("false")
            else:
                if len(items) == capacity:
                    capacity *= 2
                pos[value] = len(items)
                items.append(value)
                out.append("true")
        elif cmd == "REMOVE":
            if value not in pos:
                out.append("false")
            else:
                idx = pos.pop(value)
                items.pop(idx)
                for i in range(idx, len(items)):
                    pos[items[i]] = i
                if capacity > initialCapacity and len(items) <= capacity // 4:
                    capacity = max(initialCapacity, capacity // 2)
                out.append("true")
        else:
            out.append("false")

    return out
