# Sum all amounts, then add back 5 for each month whose card payments waive its fee.
from typing import List, Optional, Any


def solution(A: List[int], D: List[str]) -> int:
    total = sum(A)
    counts = {}
    sums = {}
    for amount, date in zip(A, D):
        if amount < 0:
            month = date[5:7]
            counts[month] = counts.get(month, 0) + 1
            sums[month] = sums.get(month, 0) + (-amount)
    fees = 0
    for m in range(1, 13):
        key = "%02d" % m
        if counts.get(key, 0) >= 3 and sums.get(key, 0) >= 100:
            continue
        fees += 5
    return total - fees
