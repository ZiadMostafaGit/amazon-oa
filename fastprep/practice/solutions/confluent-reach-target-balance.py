from typing import List, Optional, Any


def canReachBalance(transactions: List[int], target: int) -> int:
    # bitset of reachable subset sums, shifted by the total of the debits
    off = -sum(x for x in transactions if x < 0)
    hi = sum(x for x in transactions if x > 0)
    if not (-off <= target <= hi):
        return 0
    bits = 1 << off  # empty subset: sum 0
    for x in transactions:
        bits |= (bits << x) if x >= 0 else (bits >> -x)
    return 1 if (bits >> (target + off)) & 1 else 0
