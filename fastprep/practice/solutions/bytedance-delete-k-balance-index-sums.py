# Prefix/suffix alternating sums: the suffix keeps or flips its signs depending on the parity of k.
from typing import List


def firstBalancedBlock(nums: List[int], k: int) -> int:
    n = len(nums)
    alt = [v if i % 2 == 0 else -v for i, v in enumerate(nums)]
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + alt[i]
    total = pre[n]
    sign = 1 if k % 2 == 0 else -1
    for i in range(0, n - k + 1):
        suffix = total - pre[i + k]
        if pre[i] + sign * suffix == 0:
            return i
    return -1
