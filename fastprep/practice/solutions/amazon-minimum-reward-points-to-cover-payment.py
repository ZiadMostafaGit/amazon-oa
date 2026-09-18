# Greedy: redeem points from the highest-value programs first, ceiling-dividing on the last one.
from typing import List


def minimumRewardPoints(targetMicrodollars: int, balances: List[int], valueMicrodollarsPerPoint: List[int]) -> int:
    programs = sorted(zip(valueMicrodollarsPerPoint, balances), key=lambda p: -p[0])
    remaining = targetMicrodollars
    used = 0
    for value, balance in programs:
        if remaining <= 0:
            break
        if balance <= 0:
            continue
        need = -(-remaining // value)  # ceiling division
        if need <= balance:
            used += need
            remaining = 0
            break
        used += balance
        remaining -= balance * value
    if remaining > 0:
        return -1
    return used
