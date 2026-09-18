# For each index, scan rightwards counting strictly greater values until the kth is found.
from typing import List


def kthGreaterIndexes(nums: List[int], k: int) -> List[int]:
    n = len(nums)
    res = [-1] * n
    for i in range(n):
        v = nums[i]
        cnt = 0
        for j in range(i + 1, n):
            if nums[j] > v:
                cnt += 1
                if cnt == k:
                    res[i] = j + 1
                    break
    return res
