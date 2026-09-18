# DP over values with a Fenwick tree of OR-value bitmasks; only newly seen bits are expanded.
from typing import List, Optional, Any

LIMIT = 1024


def getGoodnessValue(arr: List[int]) -> List[int]:
    size = LIMIT
    tree = [0] * (size + 1)

    def update(pos: int, mask: int) -> None:
        i = pos
        while i <= size:
            tree[i] |= mask
            i += i & -i

    def query(pos: int) -> int:
        res = 0
        i = pos
        while i > 0:
            res |= tree[i]
            i -= i & -i
        return res

    reached = [0] * LIMIT   # OR-masks already fed into value v
    ending = [0] * LIMIT    # OR values achievable by a subsequence ending with value v
    started = [False] * LIMIT

    for x in arr:
        if x <= 0:
            continue
        prev = query(x - 1) if x >= 1 else 0
        add = 0
        if not started[x]:
            started[x] = True
            add |= 1 << x
        fresh = prev & ~reached[x]
        if fresh:
            reached[x] |= fresh
            m = fresh
            while m:
                low = m & -m
                b = low.bit_length() - 1
                add |= 1 << (b | x)
                m ^= low
        delta = add & ~ending[x]
        if delta:
            ending[x] |= delta
            update(x, delta)

    total = 1  # empty subsequence -> goodness 0
    for v in range(LIMIT):
        total |= ending[v]

    out = []
    idx = 0
    while total:
        low = total & -total
        out.append(low.bit_length() - 1)
        total ^= low
    return out
