# Count combinations: coins in the outer loop, so each multiset is built in one fixed coin order.
from typing import List


def change(amount: int, coins: List[int]) -> int:
    ways = [0] * (amount + 1)
    ways[0] = 1
    for c in coins:
        for a in range(c, amount + 1):    # upward: a coin may be reused
            ways[a] += ways[a - c]
    return ways[amount]
