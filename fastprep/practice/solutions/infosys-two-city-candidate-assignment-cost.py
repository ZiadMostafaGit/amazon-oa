# Exchange argument: sort by costA - costB; the half that saves most by going to A goes to A.
from typing import List, Optional, Any


def minimumTwoCityCost(costs: List[List[int]]) -> int:
    order = sorted(costs, key=lambda c: c[0] - c[1])
    half = len(costs) // 2
    return sum(c[0] for c in order[:half]) + sum(c[1] for c in order[half:])
