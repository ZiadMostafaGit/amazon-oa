# Split into maximal alternating-parity runs; a run of length k contributes k*(k+1)/2 subarrays.
from typing import List, Optional, Any


def countSawtoothSubarrays(arr: List[int]) -> int:
    n = len(arr)
    if n == 0:
        return 0
    total = 0
    run = 1
    for i in range(1, n):
        if (arr[i] & 1) != (arr[i - 1] & 1):
            run += 1
        else:
            total += run * (run + 1) // 2
            run = 1
    total += run * (run + 1) // 2
    return total
