# Greedy: count inversions needed to move all 1s (or all 0s) to one side, using running prefix counts.
from typing import List, Optional, Any


def minimumAdjacentSwaps(bits: List[int]) -> int:
    # Cost to gather all 1s to the right: for each 0 encountered, it must cross
    # every 1 already seen before it. Equivalent to counting (1,0) inversions.
    ones = 0
    ones_before_zeros = 0  # swaps to get all 0s first, then 1s
    zeros = 0
    zeros_before_ones = 0  # swaps to get all 1s first, then 0s
    for b in bits:
        if b == 1:
            ones += 1
            zeros_before_ones += zeros
        else:
            zeros += 1
            ones_before_zeros += ones
    return min(ones_before_zeros, zeros_before_ones)
