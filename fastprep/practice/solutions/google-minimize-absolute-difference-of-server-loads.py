# Subset-sum partition via a bitset (big-int shift) over reachable subset sums.
from typing import List


def minAbsDifference(loads: List[int]) -> int:
    if not loads:
        return 0
    total = sum(loads)
    offset = -sum(x for x in loads if x < 0)  # shift so every reachable sum is >= 0
    bits = 1 << offset  # bit (s + offset) set when some subset sums to s
    for x in loads:
        if x >= 0:
            bits |= bits << x
        else:
            bits |= bits >> (-x)
    best = abs(total)
    for idx, ch in enumerate(bin(bits)[:1:-1]):
        if ch == "1":
            d = abs(total - 2 * (idx - offset))
            if d < best:
                best = d
    return best
