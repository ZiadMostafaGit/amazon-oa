from typing import List


def finalPrice(prices: List[int]) -> List[str]:
    n = len(prices)
    total = 0
    full = []
    stack = []  # indices waiting for their first equal-or-lower item to the right
    disc = [0] * n
    has = [False] * n
    for i, p in enumerate(prices):
        while stack and prices[stack[-1]] >= p:
            j = stack.pop()
            disc[j] = p
            has[j] = True
        stack.append(i)
    for i, p in enumerate(prices):
        total += p - disc[i]
        if not has[i]:
            full.append(str(i))
    return [str(total), " ".join(full)]
