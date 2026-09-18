# Row-by-row merge keeping only the k smallest partial sums (heap-based pruning).
import heapq
from typing import List, Optional, Any


def solve(mat: List[List[int]], k: int) -> int:
    sums = [0]
    for row in mat:
        row = sorted(row)[:k]
        candidates = (a + b for a in sums for b in row)
        sums = heapq.nsmallest(k, candidates)
    sums.sort()
    return sums[k - 1]
