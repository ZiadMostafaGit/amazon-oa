# For each middle j: (# earlier values greater) * (# later values smaller). Two Fenwick passes over value ranks.
from typing import List


def countDecreasingTriplets(nums: List[int]) -> int:
    n = len(nums)
    if n < 3:
        return 0
    rank = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}
    m = len(rank)
    r = [rank[v] for v in nums]

    def counts(seq, want_greater):
        tree = [0] * (m + 1)
        res, seen = [], 0
        for x in seq:
            i, le = x if want_greater else x - 1, 0
            while i > 0:
                le += tree[i]
                i -= i & -i
            res.append(seen - le if want_greater else le)
            i = x
            while i <= m:
                tree[i] += 1
                i += i & -i
            seen += 1
        return res

    greater_before = counts(r, True)                  # earlier with rank > x
    smaller_after = counts(r[::-1], False)[::-1]      # later with rank < x
    return sum(g * s for g, s in zip(greater_before, smaller_after))
