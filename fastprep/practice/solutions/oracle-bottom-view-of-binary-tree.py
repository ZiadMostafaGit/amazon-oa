# BFS in level order tracking horizontal distance; later visits overwrite, so the deepest/rightmost wins.
from typing import List, Optional, Any
from collections import deque


def bottomView(root: Optional["TreeNode"]) -> List[int]:
    if root is None:
        return []
    view = {}
    q = deque([(root, 0)])
    while q:
        node, hd = q.popleft()
        view[hd] = node.val
        if node.left is not None:
            q.append((node.left, hd - 1))
        if node.right is not None:
            q.append((node.right, hd + 1))
    return [view[hd] for hd in sorted(view)]
