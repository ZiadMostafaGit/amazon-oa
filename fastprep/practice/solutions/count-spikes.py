# Two Fenwick-tree sweeps over compressed values: count strictly-smaller elements on each side.
from typing import List, Optional, Any


class _BIT:
    def __init__(self, n: int):
        self.n = n
        self.t = [0] * (n + 1)

    def add(self, i: int) -> None:
        i += 1
        while i <= self.n:
            self.t[i] += 1
            i += i & (-i)

    def query(self, i: int) -> int:
        # number of inserted values with compressed index < i
        s = 0
        while i > 0:
            s += self.t[i]
            i -= i & (-i)
        return s


def countSpikes(prices: List[int], k: int) -> int:
    n = len(prices)
    if n == 0 or k < 0:
        return 0
    vals = sorted(set(prices))
    rank = {v: i for i, v in enumerate(vals)}
    m = len(vals)

    left = [0] * n
    bit = _BIT(m)
    for i in range(n):
        r = rank[prices[i]]
        left[i] = bit.query(r)
        bit.add(r)

    bit2 = _BIT(m)
    count = 0
    for i in range(n - 1, -1, -1):
        r = rank[prices[i]]
        right = bit2.query(r)
        if left[i] >= k and right >= k:
            count += 1
        bit2.add(r)
    return count
