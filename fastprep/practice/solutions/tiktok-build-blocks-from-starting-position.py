# Keep obstacles in a sorted list; each query is a binary search for the first obstacle >= x.
from bisect import bisect_left, insort
from typing import List


def buildBlocksFromPosition(operations: List[List[int]]) -> str:
    obstacles = []
    out = []
    for op in operations:
        if op[0] == 1:
            insort(obstacles, op[1])
        else:
            x, size = op[1], op[2]
            i = bisect_left(obstacles, x)
            if i < len(obstacles) and obstacles[i] <= x + size - 1:
                out.append("0")
            else:
                out.append("1")
    return "".join(out)
