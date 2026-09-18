# Greedy: any monotone path crosses each boundary between the endpoints exactly once.
from typing import List, Optional, Any


def minCost(rows: int, cols: int, initR: int, initC: int, finalR: int, finalC: int, costRows: List[int], costCols: List[int]) -> int:
    total = 0
    for i in range(min(initR, finalR), max(initR, finalR)):
        total += costRows[i]
    for j in range(min(initC, finalC), max(initC, finalC)):
        total += costCols[j]
    return total
