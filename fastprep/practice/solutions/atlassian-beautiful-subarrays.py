# Prefix counts of odd elements plus a hash map of prefix frequencies.
from typing import List, Optional, Any
from collections import defaultdict


def beautifulSubarrays(nums: List[int], k: int) -> int:
    freq = defaultdict(int)
    freq[0] = 1
    total = 0
    odds = 0
    for v in nums:
        if v & 1:
            odds += 1
        total += freq.get(odds - k, 0)
        freq[odds] += 1
    return total
