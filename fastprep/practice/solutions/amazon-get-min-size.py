# Greedy: the n-k largest-capacity pairs come from the 2(n-k) smallest games, paired two-pointer.
from typing import List


def getMinSize(gameSize: List[int], k: int) -> int:
    a = sorted(gameSize)
    n = len(a)
    pairs = n - k           # number of pen drives that must hold two games
    best = a[-1]            # every game must fit on its own
    lo, hi = 0, 2 * pairs - 1
    while lo < hi:
        s = a[lo] + a[hi]
        if s > best:
            best = s
        lo += 1
        hi -= 1
    return best
