# Monotonic decreasing stack of (price, span) processed left to right.
from typing import List, Optional, Any


def calculateStockSpans(prices: List[int]) -> List[int]:
    stack = []  # (price, span)
    res = []
    for p in prices:
        span = 1
        while stack and stack[-1][0] <= p:
            span += stack.pop()[1]
        stack.append((p, span))
        res.append(span)
    return res
