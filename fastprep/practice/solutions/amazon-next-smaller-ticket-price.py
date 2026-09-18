# Monotonic increasing stack scanned right to left to find each next strictly smaller value.
from typing import List, Optional, Any


def nextSmallerPrices(prices: List[int]) -> List[int]:
    n = len(prices)
    res = [-1] * n
    stack = []
    for i in range(n - 1, -1, -1):
        p = prices[i]
        while stack and stack[-1] >= p:
            stack.pop()
        res[i] = stack[-1] if stack else -1
        stack.append(p)
    return res
