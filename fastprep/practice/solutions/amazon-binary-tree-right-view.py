# BFS level order, taking the last node value of each level.
from typing import List, Optional, Any
from collections import deque


def solve(root: Optional["TreeNode"]) -> List[int]:
    if root is None:
        return []
    out: List[int] = []
    q = deque([root])
    while q:
        size = len(q)
        for i in range(size):
            node = q.popleft()
            if i == size - 1:
                out.append(node.val)
            if node.left is not None:
                q.append(node.left)
            if node.right is not None:
                q.append(node.right)
    return out
