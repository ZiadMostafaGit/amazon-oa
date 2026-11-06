# For each peak, best[i] = best left-side sum ending at i with i as its top; a monotonic stack finds
# the previous smaller cap so best[i] = best[j] + maxHeights[i] * (i - j). Same from the right.
from typing import List


def maximumSumOfHeights(maxHeights: List[int]) -> int:
    n = len(maxHeights)
    left = [0] * n
    stack = []
    for i in range(n):
        while stack and maxHeights[stack[-1]] > maxHeights[i]:
            stack.pop()
        j = stack[-1] if stack else -1
        left[i] = (left[j] if j >= 0 else 0) + maxHeights[i] * (i - j)
        stack.append(i)
    right = [0] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and maxHeights[stack[-1]] > maxHeights[i]:
            stack.pop()
        j = stack[-1] if stack else n
        right[i] = (right[j] if j < n else 0) + maxHeights[i] * (j - i)
        stack.append(i)
    return max(left[i] + right[i] - maxHeights[i] for i in range(n))
