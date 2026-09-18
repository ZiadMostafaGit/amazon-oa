# Prefix-sum residue counting with a frequency table of prefix sums mod k.
from typing import List, Optional, Any


def countDivisibleSubarrays(arr: List[int], k: int) -> int:
    counts = [0] * k
    counts[0] = 1
    cur = 0
    total = 0
    for x in arr:
        cur = (cur + x) % k
        total += counts[cur]
        counts[cur] += 1
    return total
