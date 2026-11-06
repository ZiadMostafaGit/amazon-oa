# Same table, one difference: sweep amounts upward to reuse a coin (mode 0), downward to use it once (mode 1).
from typing import List


def minimumCoins(coins: List[int], amount: int, mode: int) -> int:
    INF = float("inf")
    best = [0] + [INF] * amount
    for c in coins:
        if c > amount:
            continue
        order = range(c, amount + 1) if mode == 0 else range(amount, c - 1, -1)
        for a in order:
            if best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1
    return -1 if best[amount] == INF else best[amount]
