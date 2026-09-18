# Greedy on the difference array: prefix/suffix cover decomposition, ops = (total decrease) + diff[-1].
from typing import List, Optional, Any


def getMinOperations(source: List[int], target: List[int]) -> int:
    if len(source) != len(target):
        return -1
    diff = [t - s for s, t in zip(source, target)]
    if any(d < 0 for d in diff):
        return -1
    n = len(diff)
    if n == 0:
        return 0
    # neg = minimum total decrease the non-increasing prefix-cover P must absorb
    neg = 0
    for j in range(1, n):
        if diff[j - 1] > diff[j]:
            neg += diff[j - 1] - diff[j]
    # P(0) = neg must still leave S(0) = diff[0] - neg >= 0
    if neg > diff[0]:
        return -1
    return neg + diff[n - 1]
