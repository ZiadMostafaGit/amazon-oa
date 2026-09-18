# Difference array: count riders eligible for each group size k, k feasible if count >= k.
from typing import List


def maximumCompatibleRiders(minCoRiders: List[int], maxCoRiders: List[int]) -> int:
    n = len(minCoRiders)
    diff = [0] * (n + 2)
    for i in range(n):
        lo = minCoRiders[i] + 1
        hi = maxCoRiders[i] + 1
        if hi > n:
            hi = n
        if lo > hi:
            continue
        diff[lo] += 1
        diff[hi + 1] -= 1
    best = 0
    running = 0
    for k in range(1, n + 1):
        running += diff[k]
        if running >= k:
            best = k
    return best
