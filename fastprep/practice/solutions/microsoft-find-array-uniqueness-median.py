# Binary search the answer; count subarrays with at most v distinct values
# using a sliding window.
from typing import List, Optional, Any


def findArrayUniquenessMedian(arr: List[int]) -> int:
    n = len(arr)
    total = n * (n + 1) // 2
    k = (total + 1) // 2  # 1-indexed position of the median

    def at_most(v: int) -> int:
        freq = {}
        distinct = 0
        left = 0
        result = 0
        for right in range(n):
            x = arr[right]
            c = freq.get(x, 0)
            if c == 0:
                distinct += 1
            freq[x] = c + 1
            while distinct > v:
                y = arr[left]
                freq[y] -= 1
                if freq[y] == 0:
                    distinct -= 1
                left += 1
            result += right - left + 1
        return result

    lo, hi = 1, len(set(arr))
    while lo < hi:
        mid = (lo + hi) // 2
        if at_most(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
