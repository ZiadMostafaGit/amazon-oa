from typing import List, Optional, Any
from bisect import bisect_left


def solve(arr: List[int], k: int) -> int:
    # dp[i] = longest valid subsequence ending at index i.
    # dp[i] = 1 + max(dp[j]) over j < i with arr[i] - k <= arr[j] <= arr[i] - 1.
    # A max-segment-tree keyed by compressed value answers each range max in
    # O(log n), giving O(n log n) overall.
    vals = sorted(set(arr))
    m = len(vals)
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
        # max over compressed indices [lo, hi]
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

    ans = 0
    for x in arr:
        # values in [x - k, x - 1]
        lo = bisect_left(vals, x - k)
        hi = bisect_left(vals, x) - 1
        best = query(lo, hi) + 1
        if best > ans:
            ans = best
        update(bisect_left(vals, x), best)
    return ans
