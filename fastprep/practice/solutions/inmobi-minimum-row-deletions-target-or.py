# Only submasks of target can contribute; cut the cheapest target bit by deleting all rows holding it.
from typing import List, Optional, Any


def minimumRowsToDeleteForTargetOr(rows: List[List[int]], target: int) -> int:
    if not rows:
        return 0
    width = len(rows[0])
    subs = []
    for r in rows:
        v = 0
        for b in r:
            v = (v << 1) | b
        if v & ~target == 0 and v != 0:
            subs.append(v)
    total = 0
    for v in subs:
        total |= v
    if total != target:
        return 0
    best = None
    for bit in range(width):
        mask = 1 << bit
        if target & mask:
            cnt = 0
            for v in subs:
                if v & mask:
                    cnt += 1
            if best is None or cnt < best:
                best = cnt
    return best if best is not None else 0
