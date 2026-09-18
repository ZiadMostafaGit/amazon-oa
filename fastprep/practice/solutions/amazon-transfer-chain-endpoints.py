# Approach: in-degree/out-degree counting - the start node never appears as a target, the end never as a source.
from typing import List


def solve(transfers: List[List[int]]) -> List[int]:
    sources = set()
    targets = set()
    for a, b in transfers:
        sources.add(a)
        targets.add(b)
    start = next(iter(sources - targets))
    end = next(iter(targets - sources))
    return [start, end]
