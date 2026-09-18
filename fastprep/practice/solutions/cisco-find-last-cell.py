# Walk the anti-clockwise spiral by shrinking boundaries, then take every second cell.
from typing import List


def findLastCell(matrix: List[List[int]]) -> int:
    if not matrix or not matrix[0]:
        return -1
    rows, cols = len(matrix), len(matrix[0])
    top, bottom, left, right = 0, rows - 1, 0, cols - 1
    order = []
    while top <= bottom and left <= right:
        for r in range(top, bottom + 1):
            order.append(matrix[r][left])
        left += 1
        if left > right:
            break
        for c in range(left, right + 1):
            order.append(matrix[bottom][c])
        bottom -= 1
        if top > bottom:
            break
        for r in range(bottom, top - 1, -1):
            order.append(matrix[r][right])
        right -= 1
        if left > right:
            break
        for c in range(right, left - 1, -1):
            order.append(matrix[top][c])
        top += 1
    last_hop = len(order) - 1 if len(order) % 2 == 1 else len(order) - 2
    return order[last_hop]
