# Greedy sweep with a difference array: cover each chapter's required day count using the right-most valid window.
from typing import List, Optional, Any


def findMinimumDays(pages: List[int], k: int, p: int) -> int:
    n = len(pages)
    need = [(x + p - 1) // p for x in pages]
    diff = [0] * (n + 1)
    cur = 0
    total = 0
    last_start = n - k
    for i in range(n):
        cur += diff[i]
        if cur < need[i]:
            extra = need[i] - cur
            total += extra
            cur += extra
            start = i if i < last_start else last_start
            end = start + k
            if end <= n:
                diff[end] -= extra
    return total
