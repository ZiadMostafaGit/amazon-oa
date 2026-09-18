# Sliding window over all values sorted, keeping one representative from every set.
from typing import List, Optional, Any


def minimumSelectionRange(sets: List[List[int]]) -> int:
    k = len(sets)
    if k == 0:
        return 0
    items = []
    for i, s in enumerate(sets):
        for v in s:
            items.append((v, i))
    items.sort()
    counts = [0] * k
    covered = 0
    best = None
    left = 0
    for right in range(len(items)):
        _, gi = items[right]
        if counts[gi] == 0:
            covered += 1
        counts[gi] += 1
        while covered == k:
            span = items[right][0] - items[left][0]
            if best is None or span < best:
                best = span
            lgi = items[left][1]
            counts[lgi] -= 1
            if counts[lgi] == 0:
                covered -= 1
            left += 1
    return best if best is not None else 0
