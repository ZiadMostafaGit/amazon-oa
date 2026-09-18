# Two-pointer merge of the sorted inputs, emitting a value only when it differs from the last one appended.
from typing import List, Optional, Any


def mergeSortedUnique(first: List[int], second: List[int]) -> List[int]:
    i = 0
    j = 0
    n = len(first)
    m = len(second)
    out: List[int] = []
    while i < n or j < m:
        if j >= m or (i < n and first[i] <= second[j]):
            v = first[i]
            i += 1
        else:
            v = second[j]
            j += 1
        if not out or out[-1] != v:
            out.append(v)
    return out
