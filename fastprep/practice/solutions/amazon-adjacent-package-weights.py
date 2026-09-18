# Counting sort plus greedy gap matching: weights >= 5 are pairwise incompatible, so each one
# must sit in a gap of the ascending-sorted small weights whose neighbouring small values fit.
from typing import List, Optional, Any


def canArrangePackages(weights: List[int]) -> bool:
    freq = [0] * 10
    for w in weights:
        freq[w] += 1

    # Small weights (0..4) can neighbour each other freely; big weights (5..9) cannot.
    smalls: List[int] = []
    for v in range(0, 5):
        smalls.extend([v] * freq[v])
    # Each big weight b tolerates neighbours of value at most 9 - b.
    limits: List[int] = []
    for v in range(9, 4, -1):
        limits.extend([9 - v] * freq[v])
    limits.sort()

    m = len(limits)
    if m == 0:
        return True
    k = len(smalls)
    if k == 0:
        return m <= 1

    # Placing the smalls in ascending order minimises every gap requirement:
    # gap values are s[0], s[1], ..., s[k-1] plus one more copy of the largest.
    gaps = smalls + [smalls[-1]]
    if m > len(gaps):
        return False
    for i in range(m):
        if gaps[i] > limits[i]:
            return False
    return True
