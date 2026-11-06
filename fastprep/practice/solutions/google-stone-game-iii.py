# Suffix game DP: diff[i] = best (mover - opponent) on stones i..; take 1-3 stones and subtract the opponent's best.
from typing import List


def stoneGameIII(stoneValue: List[int]) -> str:
    n = len(stoneValue)
    diff = [0] * (n + 4)
    for i in range(n - 1, -1, -1):
        best = float("-inf")
        taken = 0
        for k in range(3):
            if i + k >= n:
                break
            taken += stoneValue[i + k]
            best = max(best, taken - diff[i + k + 1])
        diff[i] = best
    return "Alice" if diff[0] > 0 else "Bob" if diff[0] < 0 else "Tie"
