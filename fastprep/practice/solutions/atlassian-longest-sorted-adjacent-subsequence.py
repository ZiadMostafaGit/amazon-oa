# Counting + scan over sorted distinct values: best total count over a maximal consecutive run.
from typing import List, Optional, Any
from collections import Counter


def longestAdjacentDifferenceSubsequence(arr: List[int]) -> int:
    freq = Counter(arr)
    vals = sorted(freq)
    best = 0
    run = 0
    prev = None
    for v in vals:
        if prev is not None and v == prev + 1:
            run += freq[v]
        else:
            run = freq[v]
        prev = v
        if run > best:
            best = run
    return best
