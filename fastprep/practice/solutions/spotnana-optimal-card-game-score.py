# Interval DP on the score difference of the player to move, then recover Alice's total.
from typing import List, Optional, Any


def maxAliceScore(cards: List[int]) -> int:
    if not cards:
        return 0
    n = len(cards)
    total = sum(cards)
    # diff[i][j] = best (current player score - other player score) on cards[i..j]
    diff = [[0] * n for _ in range(n)]
    for i in range(n):
        diff[i][i] = cards[i]
    for length in range(2, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1
            take_left = cards[i] - diff[i + 1][j]
            take_right = cards[j] - diff[i][j - 1]
            diff[i][j] = take_left if take_left > take_right else take_right
    return (total + diff[0][n - 1]) // 2
