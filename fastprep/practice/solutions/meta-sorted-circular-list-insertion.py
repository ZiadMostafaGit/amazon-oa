# Scan the serialized cycle for the first edge that can accept the value (handling the single wrap edge).
from typing import List, Optional, Any


def insertIntoSortedCircular(cycle: List[int], insertValue: int) -> List[int]:
    n = len(cycle)
    if n == 0:
        return [insertValue]
    pos = -1
    for i in range(n):
        cur = cycle[i]
        nxt = cycle[(i + 1) % n]
        if cur <= nxt:
            if cur <= insertValue <= nxt:
                pos = i
                break
        else:
            # the single descending wrap edge: it is the max -> min boundary
            if insertValue >= cur or insertValue <= nxt:
                pos = i
                break
    if pos == -1:
        # all values are equal and differ from insertValue: any edge works
        pos = n - 1
    return cycle[:pos + 1] + [insertValue] + cycle[pos + 1:]
