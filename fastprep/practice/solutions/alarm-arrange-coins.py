# Closed form: largest r with r*(r+1)/2 <= c, via integer square root.
from typing import List, Optional, Any
from math import isqrt


def arrangeCoins(coins: List[int]) -> List[int]:
    res = []
    for c in coins:
        r = (isqrt(8 * c + 1) - 1) // 2
        while (r + 1) * (r + 2) // 2 <= c:
            r += 1
        while r > 0 and r * (r + 1) // 2 > c:
            r -= 1
        res.append(r)
    return res
