# Greedy: armor saves min(armor, power[i]) on one round, so use it where that is largest.
from typing import List, Optional, Any


def getMinimumValue(power: List[int], armor: int) -> int:
    total = sum(power)
    best_save = 0
    for p in power:
        s = p if p < armor else armor
        if s > best_save:
            best_save = s
    return total - best_save + 1
