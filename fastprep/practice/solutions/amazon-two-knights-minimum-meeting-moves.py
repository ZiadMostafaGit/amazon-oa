# Closed-form infinite-board knight distance: alternating turns force m1+m2 >= d, and d is achievable.
from typing import List


def solve(first: List[int], second: List[int]) -> int:
    x = abs(first[0] - second[0])
    y = abs(first[1] - second[1])
    if x < y:
        x, y = y, x
    if x == 1 and y == 0:
        return 3
    if x == 2 and y == 2:
        return 4
    delta = x - y
    if y > delta:
        return delta - 2 * ((delta - y) // 3)
    return delta - 2 * ((delta - y) // 4)
