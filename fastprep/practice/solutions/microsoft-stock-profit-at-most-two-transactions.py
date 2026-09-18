# Approach: single-pass DP over the four states buy1/sell1/buy2/sell2.
from typing import List, Optional, Any


def maxProfitAtMostTwo(prices: List[int]) -> int:
    buy1 = buy2 = float('-inf')
    sell1 = sell2 = 0
    for p in prices:
        if -p > buy1:
            buy1 = -p
        if buy1 + p > sell1:
            sell1 = buy1 + p
        if sell1 - p > buy2:
            buy2 = sell1 - p
        if buy2 + p > sell2:
            sell2 = buy2 + p
    return int(sell2)
