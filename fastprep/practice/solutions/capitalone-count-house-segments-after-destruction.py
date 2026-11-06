from typing import List, Optional, Any


def countHouseSegmentsAfterDestruction(houses: List[int], queries: List[int]) -> List[int]:
    alive = set(houses)
    segs = sum(1 for h in alive if h - 1 not in alive)
    out = []
    for x in queries:
        alive.discard(x)
        l, r = (x - 1) in alive, (x + 1) in alive
        if l and r:
            segs += 1
        elif not l and not r:
            segs -= 1
        out.append(segs)
    return out
