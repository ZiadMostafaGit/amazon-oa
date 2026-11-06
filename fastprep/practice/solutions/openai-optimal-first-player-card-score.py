# Score difference DP over the remaining interval, then first = (total + difference) / 2.
from typing import List


def maxScore(cards: List[int]) -> int:
    n = len(cards)
    d = list(cards)
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            d[i] = max(cards[i] - d[i + 1], cards[j] - d[i])
    return (sum(cards) + d[0]) // 2
