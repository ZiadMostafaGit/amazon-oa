# Sort with prefix sums: a process survives iff every larger process beyond the last "unreachable" gap can be absorbed.
from typing import List, Optional, Any


def inventoryProcessesSurvivalPossibility(n: int, bots: List[int]) -> List[int]:
    if n <= 0 or not bots:
        return []
    order = sorted(range(n), key=lambda i: bots[i])
    # last position j (>=1) where the sum of all strictly-earlier processes cannot reach bots[j]
    last_bad = 0
    running = bots[order[0]]
    for j in range(1, n):
        v = bots[order[j]]
        if running < v:
            last_bad = j
        running += v
    result = [order[j] + 1 for j in range(last_bad, n)]
    result.sort()
    return result
