# Greedy exchange argument: start with all tasks on intern 2, then move the k tasks with the largest (reward_1 - reward_2) gain.
from typing import List


def getMaximumRewardPoints(k: int, reward_1: List[int], reward_2: List[int]) -> int:
    n = len(reward_1)
    total = sum(reward_2)
    gains = [reward_1[i] - reward_2[i] for i in range(n)]
    gains.sort(reverse=True)
    for i in range(k):
        total += gains[i]
    return total
