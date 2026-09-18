# State-machine DP (hold / cash); equivalently the sum of every positive daily gain.
from typing import List, Optional, Any


def maxProfitUnlimited(prices: List[int]) -> int:
    cash = 0
    hold = float('-inf')
    for p in prices:
        new_hold = hold if hold > cash - p else cash - p
        new_cash = cash if cash > hold + p else hold + p
        hold, cash = new_hold, new_cash
    return int(cash)
