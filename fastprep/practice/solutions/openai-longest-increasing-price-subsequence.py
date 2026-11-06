from bisect import bisect_left
from typing import List


def solve(prices: List[int]) -> int:
    tails = []
    for x in prices:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
