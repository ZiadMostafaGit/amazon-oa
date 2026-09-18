# Brute-force enumeration of all 2^n index subsets via bitmask, then lexicographic sort.
from typing import List, Optional, Any


def allSubsequences(s: str) -> List[str]:
    n = len(s)
    out = []
    for mask in range(1 << n):
        out.append("".join(s[i] for i in range(n) if mask & (1 << i)))
    out.sort()
    return out
