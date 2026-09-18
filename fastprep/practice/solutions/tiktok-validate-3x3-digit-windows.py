# Sliding window over columns with a running digit-count array (O(n) total).
from typing import List, Optional, Any


def validateDigitWindows(numbers: List[List[int]]) -> List[bool]:
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

    res: List[bool] = []
    for c in range(n):
        add(c)
        if c >= 2:
            res.append(distinct == 9)
            remove(c - 2)
    return res
