# Sliding window with per-bit counts: OR popcount grows with the right end and shrinks with
# the left end, so shrink until popcount <= mx and check the mn bound at that widest window.
from typing import List, Optional, Any


def longestGoodSubarray(arr: List[int], mn: int, mx: int) -> int:
    n = len(arr)
    if n == 0:
        return 0
    bits = max(1, max((x.bit_length() for x in arr), default=1))
    cnt = [0] * bits
    active = 0  # number of bit positions present in the window

    def add(x, delta):
        nonlocal active
        b = 0
        while x:
            if x & 1:
                if delta > 0:
                    if cnt[b] == 0:
                        active += 1
                    cnt[b] += 1
                else:
                    cnt[b] -= 1
                    if cnt[b] == 0:
                        active -= 1
            x >>= 1
            b += 1

    best = 0
    left = 0
    for right in range(n):
        add(arr[right], 1)
        while active > mx and left <= right:
            add(arr[left], -1)
            left += 1
        if left <= right and mn <= active <= mx:
            best = max(best, right - left + 1)
    return best
