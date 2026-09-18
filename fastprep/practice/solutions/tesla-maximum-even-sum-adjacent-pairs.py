# Even sum means equal parity: split the circle into maximal same-parity runs, sum floor(len/2).
from typing import List, Optional, Any


def maxEvenSumPairs(nums: List[int]) -> int:
    n = len(nums)
    par = [v & 1 for v in nums]
    start = -1
    for i in range(n):
        if par[i] != par[i - 1]:
            start = i
            break
    if start == -1:
        # whole circle is one parity: it is a single cycle, matching is floor(n/2)
        return n // 2
    total = 0
    run = 1
    for k in range(1, n):
        i = (start + k) % n
        j = (start + k - 1) % n
        if par[i] == par[j]:
            run += 1
        else:
            total += run // 2
            run = 1
    total += run // 2
    return total
