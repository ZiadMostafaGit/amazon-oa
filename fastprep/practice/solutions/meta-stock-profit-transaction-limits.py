# Greedy: sum of all positive day-to-day rises for unlimited, min-price scan for a single transaction.
from typing import List, Optional, Any


def maxStockProfit(prices: List[int], transactionLimit: int) -> int:
    if not prices or len(prices) < 2:
        return 0
    if transactionLimit == -1:
        total = 0
        for a, b in zip(prices, prices[1:]):
            if b > a:
                total += b - a
        return total
    best = 0
    lowest = prices[0]
    for p in prices[1:]:
        if p - lowest > best:
            best = p - lowest
        if p < lowest:
            lowest = p
    return best
