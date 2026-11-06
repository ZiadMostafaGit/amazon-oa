# 0/1 knapsack, one row: iterate capacity downward so each item is used at most once.
from typing import List


def maximumKnapsackValue(weights: List[int], values: List[int], capacity: int) -> int:
    best = [0] * (capacity + 1)          # best[c] = max value with total weight <= c
    for w, v in zip(weights, values):
        for c in range(capacity, w - 1, -1):
            if best[c - w] + v > best[c]:
                best[c] = best[c - w] + v
    return best[capacity]
