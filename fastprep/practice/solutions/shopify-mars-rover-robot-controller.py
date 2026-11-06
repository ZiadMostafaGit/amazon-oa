# State machine: the heading is an index into a clockwise direction table; L/R turn by -1/+1 mod 4, M steps.
from typing import List


def getRoverPosition(start: List[int], direction: str, commands: str) -> str:
    heads = "NESW"
    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]
    x, y = start[0], start[1]
    d = heads.index(direction)
    for ch in commands:
        if ch == "L":
            d = (d + 3) % 4
        elif ch == "R":
            d = (d + 1) % 4
        elif ch == "M":
            x += dx[d]
            y += dy[d]
    return "%d %d %s" % (x, y, heads[d])
