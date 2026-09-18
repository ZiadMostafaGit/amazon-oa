# BFS by level (left child before right) recording the first node seen at each horizontal distance.
from typing import List, Optional, Any
from collections import deque


def topView(root: Optional[TreeNode]) -> List[int]:
    if root is None:
        return []
    first = {}
    q = deque([(root, 0)])
    while q:
        node, hd = q.popleft()
        if hd not in first:
            first[hd] = node.val
        if node.left is not None:
            q.append((node.left, hd - 1))
        if node.right is not None:
            q.append((node.right, hd + 1))
    return [first[hd] for hd in sorted(first)]
