# Prefix XOR with a hash map of previously seen prefixes.
from typing import List, Optional, Any
from collections import defaultdict


def subarraysXor(arr: List[int], x: int) -> int:
    seen = defaultdict(int)
    seen[0] = 1
    prefix = 0
    total = 0
    for value in arr:
        prefix ^= value
        total += seen[prefix ^ x]
        seen[prefix] += 1
    return total
