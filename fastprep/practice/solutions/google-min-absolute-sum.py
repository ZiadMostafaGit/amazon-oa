# Negating x changes the total S to S - 2x, so scan every candidate x plus the no-change option.
from typing import List, Optional, Any


def solve(A: List[int]) -> int:
    total = sum(A)
    best = abs(total)
    for x in A:
        cand = abs(total - 2 * x)
        if cand < best:
            best = cand
    return best
