# Subset-sum partition via a bitset (big-int shift) over reachable subset sums.
from typing import List


def minAbsDifference(loads: List[int]) -> int:
    if not loads:
        return 0
    total = sum(loads)
    offset = -sum(x for x in loads if x < 0)  # shift so every reachable sum is >= 0
    span = sum(abs(x) for x in loads)
    if span == 0:
        return 0

    bits = 1 << offset  # reachable sums, bit (s + offset) set for subset sum s
    mask = (1 << (span * 2 + 2)) - 1
    for x in loads:
        if x >= 0:
            bits |= bits << x
        else:
            bits |= bits >> (-x)
        bits &= mask

    best = abs(total)
    s = bits
    # iterate set bits efficiently
    while s:
        low = s & -s
        idx = low.bit_length() - 1
        subset = idx - offset
        diff = abs(total - 2 * subset)
        if diff < best:
            best = diff
            if best == 0:
                return 0
        s ^= low
    return best
