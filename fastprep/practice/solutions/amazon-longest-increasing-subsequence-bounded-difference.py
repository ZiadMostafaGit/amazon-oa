# DP over compressed values with a max segment tree: dp[x] = 1 + max dp[v] for v in [x-k, x-1].
from typing import List, Optional, Any


def solve(arr: List[int], k: int) -> int:
    if not arr:
        return 0
    vals = sorted(set(arr))
    m = len(vals)
    import bisect

    size = 1
    while size < m:
        size <<= 1
    tree = [0] * (2 * size)

    def update(pos: int, value: int) -> None:
        i = pos + size
        if tree[i] >= value:
            return
        tree[i] = value
        i >>= 1
        while i:
            new = tree[2 * i] if tree[2 * i] > tree[2 * i + 1] else tree[2 * i + 1]
            if tree[i] == new:
                break
            tree[i] = new
            i >>= 1

    def query(lo: int, hi: int) -> int:
        # inclusive [lo, hi]
        if lo > hi:
            return 0
        res = 0
        lo += size
        hi += size + 1
        while lo < hi:
            if lo & 1:
                if tree[lo] > res:
                    res = tree[lo]
                lo += 1
            if hi & 1:
                hi -= 1
                if tree[hi] > res:
                    res = tree[hi]
            lo >>= 1
            hi >>= 1
        return res

    best = 0
    for x in arr:
        idx = bisect.bisect_left(vals, x)
        # values strictly less than x and >= x - k
        left = bisect.bisect_left(vals, x - k)
        cur = query(left, idx - 1) + 1
        if cur > best:
            best = cur
        update(idx, cur)
    return best
