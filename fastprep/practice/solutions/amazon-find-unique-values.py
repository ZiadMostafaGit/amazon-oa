# Sort, pair smallest with largest, and count distinct pair sums (equivalent to distinct averages).
from typing import List


def findUniqueValues(experience: List[int]) -> int:
    arr = sorted(experience)
    sums = set()
    i, j = 0, len(arr) - 1
    while i < j:
        sums.add(arr[i] + arr[j])
        i += 1
        j -= 1
    return len(sums)
