# Sort plus sliding window for the longest balanced run, then one extra element saved by the modification.
from typing import List, Optional, Any


def minimumRemovalsToBalance(arr: List[int]) -> int:
    n = len(arr)
    a = sorted(arr)
    best = 0
    i = 0
    for j in range(n):
        while a[j] > 2 * a[i]:
            i += 1
        if j - i + 1 > best:
            best = j - i + 1
    keep = best + 1 if best < n else n
    return n - keep
