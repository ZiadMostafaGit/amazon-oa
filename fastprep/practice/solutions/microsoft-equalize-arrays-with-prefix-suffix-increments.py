# Split the required delta into a non-increasing prefix profile plus a non-decreasing suffix profile; cost is d[0] plus the total rise.
from typing import List, Optional, Any


def getMinOperations(source: List[int], target: List[int]) -> int:
    n = len(source)
    d = [target[i] - source[i] for i in range(n)]
    if any(x < 0 for x in d):
        return -1
    # minimal suffix profile: accumulate the positive rises of d
    suf = 0
    if d[0] < 0:
        return -1
    total = d[0]
    prev = d[0]
    for i in range(1, n):
        rise = d[i] - prev
        if rise > 0:
            suf += rise
            total += rise
        prev = d[i]
        if d[i] - suf < 0:
            return -1
    return total
