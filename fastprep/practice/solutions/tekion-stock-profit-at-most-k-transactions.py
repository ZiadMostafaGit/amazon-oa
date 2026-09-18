# DP over transactions with rolling buy/sell states (O(n*k)).
from typing import List, Optional, Any


def maxProfit(prices: List[int], k: int) -> int:
    n = len(prices)
    if n < 2 or k <= 0:
        return 0
    if k >= n // 2:
        total = 0
        for i in range(1, n):
            if prices[i] > prices[i - 1]:
                total += prices[i] - prices[i - 1]
        return total
    NEG = float("-inf")
    buy = [NEG] * (k + 1)
    sell = [0] * (k + 1)
    for price in prices:
        for t in range(1, k + 1):
            if sell[t - 1] - price > buy[t]:
                buy[t] = sell[t - 1] - price
            if buy[t] + price > sell[t]:
                sell[t] = buy[t] + price
    return sell[k]
