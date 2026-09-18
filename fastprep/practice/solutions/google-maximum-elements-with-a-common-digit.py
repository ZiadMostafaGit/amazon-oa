# Counting: for each digit 0-9, count how many numbers contain it; take the max.
from typing import List


def solution(numbers: List[int]) -> int:
    best = 0
    for digit in "0123456789":
        count = 0
        for value in numbers:
            if digit in str(value):
                count += 1
        if count > best:
            best = count
    return best
