# Track running max of normalized (min side, max side); a rotated rectangle fits a box iff both normalized sides fit.
from typing import List, Optional, Any


def solution(operations: List[List[int]]) -> List[bool]:
    max_small = 0
    max_large = 0
    res: List[bool] = []
    for op in operations:
        kind, a, b = op[0], op[1], op[2]
        lo = a if a < b else b
        hi = b if a < b else a
        if kind == 0:
            if lo > max_small:
                max_small = lo
            if hi > max_large:
                max_large = hi
        else:
            res.append(max_small <= lo and max_large <= hi)
    return res
