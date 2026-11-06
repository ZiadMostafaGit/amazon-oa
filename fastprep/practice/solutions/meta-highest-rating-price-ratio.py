from typing import List, Optional, Any


def solution(prices: List[int], ratings: List[int]) -> int:
    best = 0
    for i in range(1, len(prices)):
        # ratings[i]/prices[i] > ratings[best]/prices[best], compared exactly
        if ratings[i] * prices[best] > ratings[best] * prices[i]:
            best = i
    return best
