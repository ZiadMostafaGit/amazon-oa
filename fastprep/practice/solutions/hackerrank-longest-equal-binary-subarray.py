# Prefix sum with 0 mapped to -1; first occurrence of each running balance in a hash map.
from typing import List


def longestEqualBinarySubarray(arr: List[int]) -> int:
    first = {0: -1}
    balance = 0
    best = 0
    for i, v in enumerate(arr):
        balance += 1 if v == 1 else -1
        if balance in first:
            length = i - first[balance]
            if length > best:
                best = length
        else:
            first[balance] = i
    return best
