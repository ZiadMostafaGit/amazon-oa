# Sliding window with a frequency map, shrinking from the left while the window still holds k distinct values.
from typing import List, Optional, Any


def findMinimumLengthSubarray(arr: List[int], k: int) -> int:
    freq = {}
    distinct = 0
    best = -1
    left = 0
    for right, value in enumerate(arr):
        c = freq.get(value, 0)
        if c == 0:
            distinct += 1
        freq[value] = c + 1

        while distinct >= k:
            length = right - left + 1
            if best == -1 or length < best:
                best = length
            lv = arr[left]
            freq[lv] -= 1
            if freq[lv] == 0:
                distinct -= 1
            left += 1
    return best
