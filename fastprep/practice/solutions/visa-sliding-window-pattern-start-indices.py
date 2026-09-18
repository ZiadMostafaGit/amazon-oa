# KMP failure-function search reporting every (possibly overlapping) match start in linear time.
from typing import List


def findPatternStartIndices(sequence: str, pattern: str) -> List[int]:
    n, m = len(sequence), len(pattern)
    if m == 0 or m > n:
        return []
    fail = [0] * m
    k = 0
    for i in range(1, m):
        while k and pattern[i] != pattern[k]:
            k = fail[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        fail[i] = k
    res = []
    k = 0
    for i in range(n):
        ch = sequence[i]
        while k and ch != pattern[k]:
            k = fail[k - 1]
        if ch == pattern[k]:
            k += 1
            if k == m:
                res.append(i - m + 1)
                k = fail[k - 1]
    return res
