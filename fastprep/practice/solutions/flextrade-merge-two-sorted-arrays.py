# Two-pointer merge of two already sorted arrays.
from typing import List, Optional, Any


def mergeSortedArrays(first: List[int], second: List[int]) -> List[int]:
    i = j = 0
    n, m = len(first), len(second)
    out = []
    while i < n and j < m:
        if first[i] <= second[j]:
            out.append(first[i])
            i += 1
        else:
            out.append(second[j])
            j += 1
    if i < n:
        out.extend(first[i:])
    if j < m:
        out.extend(second[j:])
    return out
