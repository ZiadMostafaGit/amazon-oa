from typing import List, Optional, Any


def solve(prices: List[int]) -> List[int]:
    # Monotonic decreasing stack of indices; each day pops all earlier days
    # whose price is <= today's, inheriting their spans.  O(n) total.
    n = len(prices)
    spans = [0] * n
    stack = []  # indices with strictly decreasing prices
    for i in range(n):
        while stack and prices[stack[-1]] <= prices[i]:
            stack.pop()
        spans[i] = i + 1 if not stack else i - stack[-1]
        stack.append(i)
    return spans
