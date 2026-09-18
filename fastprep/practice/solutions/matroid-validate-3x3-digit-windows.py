# Sliding window over columns with a digit-count array updated in O(1) per shift.
from typing import List, Optional, Any


def solution(numbers: List[List[int]]) -> List[bool]:
    n = len(numbers[0])
    counts = [0] * 10
    distinct = 0

    def add(col: int) -> None:
        nonlocal distinct
        for r in range(3):
            d = numbers[r][col]
            if counts[d] == 0:
                distinct += 1
            counts[d] += 1

    def remove(col: int) -> None:
        nonlocal distinct
        for r in range(3):
            d = numbers[r][col]
            counts[d] -= 1
            if counts[d] == 0:
                distinct -= 1

    for c in range(3):
        add(c)

    res = [distinct == 9]
    for c in range(3, n):
        add(c)
        remove(c - 3)
        res.append(distinct == 9)
    return res
