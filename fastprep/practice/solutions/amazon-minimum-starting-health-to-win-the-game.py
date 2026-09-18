# Greedy: total damage minus the best single armor saving, plus one to stay above zero.
from typing import List, Optional, Any


def minimumStartingHealth(power: List[int], armor: int) -> int:
    total = 0
    best_save = 0
    for p in power:
        total += p
        save = p if p < armor else armor
        if save > best_save:
            best_save = save
    return total - best_save + 1
