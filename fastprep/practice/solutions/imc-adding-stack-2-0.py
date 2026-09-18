# Lazy increment array plus a running sum, giving O(1) per operation.
from typing import List, Optional, Any


def processAddingStack(operations: List[str]) -> List[int]:
    vals = []
    lazy = []
    total = 0
    out = []
    for op in operations:
        parts = op.split()
        cmd = parts[0]
        if cmd == "push":
            v = int(parts[1])
            vals.append(v)
            lazy.append(0)
            total += v
        elif cmd == "pop":
            k = len(vals) - 1
            total -= vals[k] + lazy[k]
            if k > 0:
                lazy[k - 1] += lazy[k]
            vals.pop()
            lazy.pop()
        else:  # inc i v
            i = int(parts[1])
            v = int(parts[2])
            if i > 0:
                total += i * v
                lazy[i - 1] += v
        out.append(total)
    return out
