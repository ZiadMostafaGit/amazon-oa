# Greedy zig-zag: sort, then alternate largest / smallest so every jump spans the widest gap.
from typing import List


def findMaximumCalories(height: List[int]) -> int:
    a = sorted(height)
    lo, hi = 0, len(a) - 1
    order = []
    take_high = True
    while lo <= hi:
        if take_high:
            order.append(a[hi])
            hi -= 1
        else:
            order.append(a[lo])
            lo += 1
        take_high = not take_high
    total = order[0] * order[0]  # jump from the ground (height 0)
    for i in range(len(order) - 1):
        d = order[i] - order[i + 1]
        total += d * d
    return total
