# Largest rectangle in a histogram, but each candidate rectangle (height h, width w) holds a square of side min(h, w).
from typing import List


def largetstSquareArea(cityline: List[int]) -> int:
    best = 0
    stack = []  # indices with increasing heights
    h = list(cityline) + [0]
    for i, x in enumerate(h):
        while stack and h[stack[-1]] >= x:
            j = stack.pop()
            left = stack[-1] + 1 if stack else 0
            side = min(h[j], i - left)
            best = max(best, side * side)
        stack.append(i)
    return best
