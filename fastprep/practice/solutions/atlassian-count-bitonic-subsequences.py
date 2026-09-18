# Counting DP with a Fenwick tree over values: inc[i]*dec[i] per peak, minus the empty sides.
from typing import List, Optional, Any

MOD = 10 ** 9 + 7


class _BIT:
    def __init__(self, n: int):
        self.n = n
        self.t = [0] * (n + 1)

    def add(self, i: int, v: int) -> None:
        while i <= self.n:
            self.t[i] = (self.t[i] + v) % MOD
            i += i & (-i)

    def sum(self, i: int) -> int:
        s = 0
        while i > 0:
            s = (s + self.t[i]) % MOD
            i -= i & (-i)
        return s


def countBitonicSubsequences(arr: List[int]) -> int:
    n = len(arr)
    if n < 3:
        return 0
    maxv = max(arr)
    size = maxv + 1

    # inc[i]: number of strictly increasing subsequences ending at i (incl. singleton)
    inc = [1] * n
    bit = _BIT(size)
    for i, v in enumerate(arr):
        inc[i] = (1 + bit.sum(v - 1)) % MOD
        bit.add(v, inc[i])

    # dec[i]: number of strictly decreasing subsequences starting at i (incl. singleton)
    dec = [1] * n
    bit2 = _BIT(size)
    for i in range(n - 1, -1, -1):
        v = arr[i]
        dec[i] = (1 + bit2.sum(v - 1)) % MOD
        bit2.add(v, dec[i])

    total = 0
    for i in range(n):
        total = (total + (inc[i] - 1) * (dec[i] - 1)) % MOD
    return total % MOD
