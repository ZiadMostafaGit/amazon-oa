# Hash the stop names to their positions; the fare is the absolute index distance.
from typing import List, Optional, Any


def solve(route: List[str], start: str, stop: str) -> int:
    position = {}
    for i, name in enumerate(route):
        if name not in position:
            position[name] = i
    if start not in position or stop not in position:
        return -1
    return abs(position[start] - position[stop])
