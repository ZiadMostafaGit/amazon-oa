# Single pass bucket count: fail (<50), pass (50..80), honors (>80).
from typing import List, Optional, Any


def solve(scores: List[int]) -> List[int]:
    fail = regular = honors = 0
    for s in scores:
        if s < 50:
            fail += 1
        elif s <= 80:
            regular += 1
        else:
            honors += 1
    return [fail, regular, honors]
