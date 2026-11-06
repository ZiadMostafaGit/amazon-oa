from typing import List


def equilibriumIndex(values: List[int]) -> int:
    total = sum(values)
    left = 0
    for i, v in enumerate(values):
        if left == total - left - v:
            return i
        left += v
    return -1
