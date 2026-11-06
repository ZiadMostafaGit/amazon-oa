# Compress values to ranks, then scan right to left counting smaller values already seen (Fenwick tree).
from typing import List


def countInversions(nums: List[int]) -> int:
    rank = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}
    m = len(rank)
    tree = [0] * (m + 1)
    total = 0
    for v in reversed(nums):
        r = rank[v]
        i = r - 1
        while i > 0:
            total += tree[i]
            i -= i & -i
        i = r
        while i <= m:
            tree[i] += 1
            i += i & -i
    return total
