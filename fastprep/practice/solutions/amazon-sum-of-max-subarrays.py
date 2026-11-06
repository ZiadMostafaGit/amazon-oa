# Contribution: arr[i] is the maximum of every subarray [l, r] with L < l <= i <= r < R,
# where L is the previous index with value >= arr[i] and R the next with value > arr[i].
# The total length of those subarrays is sum over l, r of (r - l + 1) = a*b*(b+1)/2 + b*a*(a-1)/2,
# with a = i - L choices of l and b = R - i choices of r.
from typing import List


def sumOfMaxOfSubarrays(arr: List[int]) -> int:
    n = len(arr)
    left = [-1] * n
    right = [n] * n
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] < arr[i]:
            right[stack.pop()] = i
        left[i] = stack[-1] if stack else -1
        stack.append(i)
    total = 0
    for i in range(n):
        a = i - left[i]
        b = right[i] - i
        # sum over l in [i-a+1, i], r in [i, i+b-1] of (r - l + 1)
        # = sum over p in [0,a), q in [0,b) of (p + q + 1)
        lengths = b * a * (a - 1) // 2 + a * b * (b - 1) // 2 + a * b
        total += arr[i] * lengths
    return total
