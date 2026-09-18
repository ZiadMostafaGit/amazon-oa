# Canonical form via minimal string rotation: group equal canonical forms and count pairs.
from typing import List, Optional, Any
from collections import Counter


def _canonical(n: int) -> str:
    s = str(n)
    d = s + s
    L = len(s)
    best = None
    for i in range(L):
        r = d[i:i + L]
        if best is None or r < best:
            best = r
    return str(L) + ":" + best


def solution(a: List[int]) -> int:
    counts = Counter(_canonical(x) for x in a)
    return sum(c * (c - 1) // 2 for c in counts.values())
