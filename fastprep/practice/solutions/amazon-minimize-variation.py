# Interval DP over sorted values: every optimal prefix set is a contiguous sorted window.
from typing import List


def minimizeVariation(productSize: List[int]) -> int:
    a = sorted(productSize)
    n = len(a)
    if n <= 1:
        return 0

    # prev[l] = best cost of prefixes up to the window a[l .. l+length-2]
    prev = [0] * n
    for length in range(2, n + 1):
        cur = [0] * (n - length + 1)
        for l in range(n - length + 1):
            r = l + length - 1
            # extend the window left (from [l+1, r]) or right (from [l, r-1])
            best = prev[l + 1] if prev[l + 1] < prev[l] else prev[l]
            cur[l] = (a[r] - a[l]) + best
        prev = cur
    return prev[0]
