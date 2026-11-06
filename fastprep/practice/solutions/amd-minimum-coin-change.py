# best[a] = 1 + min over coins c <= a of best[a - c]; best[0] = 0.
from typing import List, Optional, Any


def minimumCoins(coins: List[int], amount: int) -> int:
    INF = float("inf")
    best = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1
    return -1 if best[amount] == INF else best[amount]
