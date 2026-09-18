# In-place cyclic sort: put each value v in 1..n at index v-1, then scan for the first mismatch.
from typing import List, Optional, Any


def solve(nums: List[int]) -> int:
    n = len(nums)
    arr = list(nums)
    for i in range(n):
        while 1 <= arr[i] <= n and arr[arr[i] - 1] != arr[i]:
            j = arr[i] - 1
            arr[i], arr[j] = arr[j], arr[i]
    for i in range(n):
        if arr[i] != i + 1:
            return i + 1
    return n + 1
