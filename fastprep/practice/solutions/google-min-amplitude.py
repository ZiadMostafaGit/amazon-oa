# Sort; changing up to 3 values = dropping some from the low end and the rest from the high end. Try the 4 splits. O(n log n).
from typing import List, Optional, Any


def minAmplitude(A: List[int]) -> int:
    n = len(A)
    if n <= 4:
        return 0
    a = sorted(A)
    return min(a[n - 4 + i] - a[i] for i in range(4))
