# Approach: precompute a prefix-sum table of "no repeated digit" counts up to the max bound, answer each query in O(1).
from typing import List, Optional, Any


def _has_unique_digits(x: int) -> bool:
    mask = 0
    while x > 0:
        bit = 1 << (x % 10)
        if mask & bit:
            return False
        mask |= bit
        x //= 10
    return True


def countNumbers(arr: List[List[int]]) -> List[int]:
    if not arr:
        return []
    hi = 0
    for row in arr:
        if row[1] > hi:
            hi = row[1]
        if row[0] > hi:
            hi = row[0]
    prefix = [0] * (hi + 2)
    for value in range(1, hi + 1):
        prefix[value] = prefix[value - 1] + (1 if _has_unique_digits(value) else 0)
    out = []
    for row in arr:
        n, m = row[0], row[1]
        if n > m:
            n, m = m, n
        lo = max(n, 1)
        if lo > m:
            out.append(0)
        else:
            out.append(prefix[m] - prefix[lo - 1])
    return out
