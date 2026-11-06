# Equal partition = some subset sums to total/2 (equivalently: +/- signs that sum to 0).
from typing import List


def equalPartition(values: List[int]) -> bool:
    total = sum(values)
    if total % 2:
        return False
    half = total // 2
    mask = (1 << (half + 1)) - 1
    reach = 1
    for v in values:
        reach |= (reach << v) & mask
    return bool((reach >> half) & 1)
