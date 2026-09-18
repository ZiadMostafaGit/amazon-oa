# Bucket values by residue mod x; walk 0,1,2,... consuming one element of residue m % x each step.
from typing import List, Optional, Any


def maximumMEX(arr: List[int], x: int) -> int:
    counts = [0] * x
    for v in arr:
        counts[v % x] += 1
    mex = 0
    while True:
        r = mex % x
        if counts[r] == 0:
            return mex
        counts[r] -= 1
        mex += 1
