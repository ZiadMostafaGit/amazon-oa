# Greedy over frequency counts: use as many groups of three as possible per weight.
from typing import List
from collections import Counter


def findMinTrips(packageweight: List[int]) -> int:
    trips = 0
    for count in Counter(packageweight).values():
        if count == 1:
            return -1
        trips += (count + 2) // 3
    return trips
