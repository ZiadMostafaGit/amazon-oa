# DFS collecting (col, row, val) triples, then sort and group by column.
from typing import List, Optional, Any


def verticalTraversal(root: Optional[TreeNode]) -> List[List[int]]:
    nodes = []

    stack = [(root, 0, 0)]
    while stack:
        node, row, col = stack.pop()
        if node is None:
            continue
        nodes.append((col, row, node.val))
        stack.append((node.left, row + 1, col - 1))
        stack.append((node.right, row + 1, col + 1))

    nodes.sort()
    res = []
    prev_col = None
    for col, _row, val in nodes:
        if col != prev_col:
            res.append([])
            prev_col = col
        res[-1].append(val)
    return res
