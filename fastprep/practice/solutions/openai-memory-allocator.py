# Maintain a sorted list of free intervals; scan it for first-fit / best-fit and merge neighbours on free.
from typing import List, Optional, Any
import bisect


def simulateMemoryAllocator(n: int, strategy: str, operations: List[str]) -> List[str]:
    free = [(0, n)]  # (start, length), sorted by start, non-adjacent
    allocated = {}   # start -> length
    out: List[str] = []
    best = strategy == "best_fit"

    for op in operations:
        parts = op.split()
        cmd = parts[0]
        val = int(parts[1])
        if cmd == "malloc":
            k = val
            idx = -1
            if best:
                bl = None
                for i, (s, ln) in enumerate(free):
                    if ln >= k and (bl is None or ln < bl):
                        bl = ln
                        idx = i
                        if ln == k:
                            break
            else:
                for i, (s, ln) in enumerate(free):
                    if ln >= k:
                        idx = i
                        break
            if idx < 0:
                out.append("-1")
                continue
            s, ln = free[idx]
            if ln == k:
                free.pop(idx)
            else:
                free[idx] = (s + k, ln - k)
            allocated[s] = k
            out.append(str(s))
        else:
            p = val
            ln = allocated.pop(p, None)
            if ln is None:
                out.append("INVALID")
                continue
            start, length = p, ln
            i = bisect.bisect_left(free, (start, 0))
            # merge with the following free block
            if i < len(free) and free[i][0] == start + length:
                length += free[i][1]
                free.pop(i)
            # merge with the preceding free block
            if i > 0 and free[i - 1][0] + free[i - 1][1] == start:
                start = free[i - 1][0]
                length += free[i - 1][1]
                free.pop(i - 1)
                i -= 1
            free.insert(i, (start, length))
            out.append("OK")
    return out
