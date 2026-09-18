# Greedy two-pointer over fish and baits sorted descending, each bait limited to 3 catches.
from typing import List, Optional, Any


def countCaughtFish(fish: List[int], baits: List[int]) -> int:
    fish_desc = sorted(fish, reverse=True)
    baits_desc = sorted(baits, reverse=True)
    n = len(fish_desc)
    j = 0
    caught = 0
    for bait in baits_desc:
        if j >= n:
            break
        used = 0
        while used < 3 and j < n and fish_desc[j] > bait:
            j += 1
            used += 1
            caught += 1
    return caught
