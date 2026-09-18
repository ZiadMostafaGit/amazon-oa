# Sort both descending and sweep with a single pointer, each bait consuming up to 3 fish.
from typing import List


def countCaughtFish(fish: List[int], baits: List[int]) -> int:
    fish_sorted = sorted(fish, reverse=True)
    n = len(fish_sorted)
    i = 0
    caught = 0
    for bait in sorted(baits, reverse=True):
        for _ in range(3):
            if i < n and fish_sorted[i] > bait:
                i += 1
                caught += 1
            else:
                break
        if i >= n:
            break
    return caught
