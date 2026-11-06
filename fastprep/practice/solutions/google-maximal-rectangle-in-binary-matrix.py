# Each row is the floor of a histogram whose bar heights are the runs of 1s ending at that row;
# the answer is the best "largest rectangle in a histogram" over all rows. O(rows * cols).
from typing import List


def maximalRectangle(matrix: List[List[int]]) -> int:
    if not matrix or not matrix[0]:
        return 0
    cols = len(matrix[0])
    heights = [0] * cols
    best = 0
    for row in matrix:
        for j in range(cols):
            heights[j] = heights[j] + 1 if row[j] == 1 else 0
        stack = []  # indices with increasing heights
        for i in range(cols + 1):
            h = heights[i] if i < cols else 0
            while stack and heights[stack[-1]] >= h:
                top = heights[stack.pop()]
                left = stack[-1] + 1 if stack else 0
                best = max(best, top * (i - left))
            stack.append(i)
    return best
