# Greedy: sort ascending, extend group count whenever the running total covers 1+2+...+(k+1).
from typing import List, Optional, Any


def maxBatchesForShipment(inventory: List[int]) -> int:
    total = 0
    groups = 0
    for x in sorted(inventory):
        total += x
        need = (groups + 1) * (groups + 2) // 2
        if total >= need:
            groups += 1
    return groups
