# Hashing: for each element generate every value reachable by at most one digit swap, look them up in a counter of earlier values.
from typing import List, Optional, Any
from collections import Counter


def _variants(value: int) -> set:
    s = str(value)
    out = {value}
    n = len(s)
    for a in range(n):
        for b in range(a + 1, n):
            if s[a] == s[b]:
                continue
            lst = list(s)
            lst[a], lst[b] = lst[b], lst[a]
            out.add(int("".join(lst)))
    return out


def countDistinctPairs(nums: List[int]) -> int:
    seen = Counter()
    total = 0
    for v in nums:
        for cand in _variants(v):
            total += seen[cand]
        seen[v] += 1
    return total
