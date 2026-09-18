# Fold each parity subsequence left to right, alternating multiply/add, all arithmetic mod 2.
from typing import List, Optional, Any


def _fold(vals: List[int]) -> int:
    if not vals:
        return 0
    r = vals[0] % 2
    for i in range(1, len(vals)):
        v = vals[i] % 2
        if i % 2 == 1:
            r = (r * v) % 2
        else:
            r = (r + v) % 2
    return r


def plusMultArray(A: List[int]) -> str:
    r_even = _fold(A[0::2])
    r_odd = _fold(A[1::2])
    if r_odd > r_even:
        return "ODD"
    if r_even > r_odd:
        return "EVEN"
    return "NEUTRAL"
