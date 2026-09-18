# Prefix-sum of (ones - zeros): longest window whose difference is 0 or +/-2 (one flip fixes +/-2).
from typing import List


def longestEqualBinarySubarrayAfterOneFlip(arr: List[int]) -> int:
    first = {0: 0}
    diff = 0
    best = 0
    for i, v in enumerate(arr, 1):
        diff += 1 if v == 1 else -1
        for want in (diff, diff - 2, diff + 2):
            j = first.get(want)
            if j is not None and i - j > best:
                best = i - j
        if diff not in first:
            first[diff] = i
    return best
