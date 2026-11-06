# Fenwick tree over value ranks: before inserting nums[i], the prefix count of smaller ranks answers it.
from typing import List


def countSmallerBefore(nums: List[int]) -> List[int]:
    rank = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}
    m = len(rank)
    tree = [0] * (m + 1)
    out = []
    for v in nums:
        r = rank[v]
        i, s = r - 1, 0                 # count of ranks 1..r-1
        while i > 0:
            s += tree[i]
            i -= i & -i
        out.append(s)
        i = r
        while i <= m:
            tree[i] += 1
            i += i & -i
    return out
