from typing import List, Optional, Any
from bisect import bisect_left, insort


def buildingBlocks(operations: List[List[int]]) -> str:
    # A block [x, x+size-1] is free iff the first obstacle >= x is beyond x+size-1.
    obstacles = []
    out = []
    for op in operations:
        if op[0] == 1:
            insort(obstacles, op[1])
        else:
            x, size = op[1], op[2]
            i = bisect_left(obstacles, x)
            out.append("1" if i == len(obstacles) or obstacles[i] > x + size - 1 else "0")
    return "".join(out)
