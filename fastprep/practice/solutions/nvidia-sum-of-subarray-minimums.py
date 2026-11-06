# Contribution: arr[i] is the minimum of (i - left) * (right - i) subarrays,
# with a strict bound on one side and a non-strict one on the other so ties count once.
from typing import List


def sumSubarrayMins(arr: List[int]) -> int:
    MOD = 10 ** 9 + 7
    n = len(arr)
    left = [-1] * n   # previous index with value < arr[i]
    right = [n] * n   # next index with value <= arr[i]
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            right[stack.pop()] = i
        left[i] = stack[-1] if stack else -1
        stack.append(i)
    total = 0
    for i in range(n):
        total += arr[i] * (i - left[i]) * (right[i] - i)
    return total % MOD
