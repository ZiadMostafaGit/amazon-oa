# Single pass over maximal runs for indicator 1, direct index probe per k for indicator 2.
from typing import List, Optional, Any


def difference_calculator(n: int, arr: List[int]) -> int:
    n = len(arr)
    ind1 = 0
    i = 0
    while i < n:
        j = i
        while j < n and arr[j] == arr[i]:
            j += 1
        if j - i == arr[i]:
            ind1 += 1
        i = j
    ind2 = 0
    for k in range(1, n + 1):
        start = k - 1
        end = start + k
        if end > n:
            break
        if all(arr[p] == k for p in range(start, end)):
            if end == n or arr[end] != k:
                ind2 += 1
    return abs(ind1 - ind2)
