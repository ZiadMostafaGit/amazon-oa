# Union of intervals via a hash map holding the run length at each segment endpoint.
from typing import List, Optional, Any


def solution(queries: List[int]) -> List[int]:
    lengths = {}
    best = 0
    out: List[int] = []
    for x in queries:
        if x in lengths:
            out.append(best)
            continue
        left = lengths.get(x - 1, 0)
        right = lengths.get(x + 1, 0)
        total = left + right + 1
        lengths[x] = total
        lengths[x - left] = total
        lengths[x + right] = total
        if total > best:
            best = total
        out.append(best)
    return out
