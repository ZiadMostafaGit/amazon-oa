# Try both alternating parity patterns; per element count halvings until parity matches.
from typing import List


def _cost(v: int, target: int) -> int:
    ops = 0
    while v % 2 != target:
        v //= 2
        ops += 1
    return ops


def minHalvingsForAlternatingParity(nums: List[int]) -> int:
    best = None
    for start in (0, 1):
        total = 0
        for i, v in enumerate(nums):
            total += _cost(v, (start + i) % 2)
        if best is None or total < best:
            best = total
    return best if best is not None else 0
