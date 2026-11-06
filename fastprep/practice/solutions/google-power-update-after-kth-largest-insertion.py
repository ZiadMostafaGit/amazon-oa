from typing import List, Optional, Any


def powerAfterInsertions(nums: List[int], p: int, queries: List[List[int]]) -> List[int]:
    MOD = 10**9 + 7
    vals = sorted(set(nums) | {v for v, _ in queries}, reverse=True)  # rank 1 = largest
    idx = {v: i + 1 for i, v in enumerate(vals)}
    m = len(vals)
    bit = [0] * (m + 1)

    def add(i):
        while i <= m:
            bit[i] += 1
            i += i & -i

    LOG = 1 << m.bit_length()

    def kth(k):  # smallest rank whose prefix count reaches k
        pos, step = 0, LOG
        while step:
            nxt = pos + step
            if nxt <= m and bit[nxt] < k:
                pos = nxt
                k -= bit[nxt]
            step >>= 1
        return pos + 1

    for v in nums:
        add(idx[v])
    out = []
    for v, k in queries:
        add(idx[v])
        x = vals[kth(k) - 1]
        p = pow(p, x, MOD)
        out.append(p)
    return out
