# Drop zeros, count inversions for both block orders (2-before-1 pairs vs 1-before-2 pairs), take the min.
from typing import List, Optional, Any


def minimumPaidSwaps(values: List[int]) -> int:
    ones_before_twos = 0  # cost to put twos first: pairs (1 ... 2)
    twos_before_ones = 0  # cost to put ones first: pairs (2 ... 1)
    seen_ones = 0
    seen_twos = 0
    for v in values:
        if v == 1:
            twos_before_ones += seen_twos
            seen_ones += 1
        elif v == 2:
            ones_before_twos += seen_ones
            seen_twos += 1
    return min(ones_before_twos, twos_before_ones)
