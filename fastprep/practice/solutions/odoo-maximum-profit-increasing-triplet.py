# Two max-prefix Fenwick trees over compressed prices: best left and best right profit per middle day.
from typing import List, Optional, Any

NEG = float("-inf")


class MaxBIT:
    __slots__ = ("n", "t")

    def __init__(self, n: int):
        self.n = n
        self.t = [NEG] * (n + 1)

    def update(self, i: int, v: int) -> None:
        i += 1
        while i <= self.n:
            if v > self.t[i]:
                self.t[i] = v
            i += i & (-i)

    def query(self, i: int):
        # max over positions [0, i] (0-based inclusive); i < 0 -> NEG
        res = NEG
        i += 1
        while i > 0:
            if self.t[i] > res:
                res = self.t[i]
            i -= i & (-i)
        return res


def getMaximumProfit(price: List[int], profit: List[int]) -> int:
    n = len(price)
    if n < 3:
        return -1

    order = sorted(set(price))
    rank = {p: idx for idx, p in enumerate(order)}
    m = len(order)

    left = [NEG] * n
    bit = MaxBIT(m)
    for j in range(n):
        r = rank[price[j]]
        left[j] = bit.query(r - 1)
        bit.update(r, profit[j])

    right = [NEG] * n
    bit2 = MaxBIT(m)
    for j in range(n - 1, -1, -1):
        r = rank[price[j]]
        # positions with rank > r  ->  mirrored index m-1-r-1
        right[j] = bit2.query(m - 1 - (r + 1))
        bit2.update(m - 1 - r, profit[j])

    best = NEG
    for j in range(n):
        if left[j] is not NEG and right[j] is not NEG and left[j] != NEG and right[j] != NEG:
            total = left[j] + profit[j] + right[j]
            if total > best:
                best = total
    return -1 if best == NEG else int(best)
