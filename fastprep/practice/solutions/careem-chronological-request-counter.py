# Sorted append-only timestamp log with binary search for the window lower bound.
from bisect import bisect_left
from typing import List, Optional, Any


def processRequestOperations(operations: List[List[str]]) -> List[int]:
    adds = []
    res = []
    for op in operations:
        if op[0] == "ADD":
            adds.append(int(op[1]))
        else:
            t = int(op[1])
            n = int(op[2])
            lo = t - 60 * n
            i = bisect_left(adds, lo)
            j = bisect_left(adds, t + 1)
            res.append(j - i)
    return res
