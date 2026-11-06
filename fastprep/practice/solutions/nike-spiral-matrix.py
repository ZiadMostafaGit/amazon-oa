from typing import List, Optional, Any


def spiralOrder(matrix: List[List[int]]) -> List[int]:
    if not matrix or not matrix[0]:
        return []
    top, bot, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    out = []
    while top <= bot and left <= right:
        for c in range(left, right + 1):
            out.append(matrix[top][c])
        for r in range(top + 1, bot + 1):
            out.append(matrix[r][right])
        if top < bot:
            for c in range(right - 1, left - 1, -1):
                out.append(matrix[bot][c])
        if left < right:
            for r in range(bot - 1, top, -1):
                out.append(matrix[r][left])
        top += 1; bot -= 1; left += 1; right -= 1
    return out
