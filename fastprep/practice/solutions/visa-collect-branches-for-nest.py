# Two outward-moving pointers from the start index, alternating right/left and skipping exhausted sides.
from typing import List, Optional, Any


def collectBranches(forest: List[int], n: int) -> List[int]:
    m = len(forest)
    r = n + 1
    l = n - 1
    picked = []
    total = 0
    want_right = True
    while total < 100:
        while r < m and forest[r] <= 0:
            r += 1
        while l >= 0 and forest[l] <= 0:
            l -= 1
        right_ok = r < m
        left_ok = l >= 0
        if not right_ok and not left_ok:
            break
        if want_right:
            take_right = right_ok
        else:
            take_right = not left_ok
        if take_right:
            picked.append(r)
            total += forest[r]
            r += 1
        else:
            picked.append(l)
            total += forest[l]
            l -= 1
        want_right = not want_right
    return picked
