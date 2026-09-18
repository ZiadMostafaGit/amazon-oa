# Greedy left-to-right cut using prefix sums: a segment stays valid while P[i+1] >= max(P[start..i-1]).
from typing import List, Optional, Any


def getMinOperations(arr: List[int]) -> int:
    n = len(arr)
    prefix = [0] * (n + 1)
    for i, v in enumerate(arr):
        prefix[i + 1] = prefix[i] + v

    NEG = float('-inf')
    ops = 0
    start = 0
    cur_max = NEG
    for i in range(n):
        if i > start:
            if prefix[i - 1] > cur_max:
                cur_max = prefix[i - 1]
            if prefix[i + 1] < cur_max:
                # Some subarray ending at i has a negative sum; overwrite arr[i] with a
                # huge positive value, which makes every subarray touching i non-negative.
                ops += 1
                start = i + 1
                cur_max = NEG
    return ops
