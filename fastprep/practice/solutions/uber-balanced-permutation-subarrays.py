# Running min/max position of values 1..k: balanced iff max - min + 1 == k.
from typing import List, Optional, Any


def countBalancedNumbers(p: List[int]) -> str:
    n = len(p)
    pos = [0] * (n + 1)
    for i, v in enumerate(p):
        pos[v] = i
    lo = n
    hi = -1
    out = []
    for k in range(1, n + 1):
        i = pos[k]
        if i < lo:
            lo = i
        if i > hi:
            hi = i
        out.append('1' if hi - lo + 1 == k else '0')
    return ''.join(out)
