# Level-order BFS: the last node of each level is the one seen from the right.
from collections import deque
from typing import List, Optional, Any


def rightSideView(root: Optional["TreeNode"]) -> List[int]:
    if root is None:
        return []
    out = []
    q = deque([root])
    while q:
        for i in range(len(q)):
            node = q.popleft()
            if node.left is not None:
                q.append(node.left)
            if node.right is not None:
                q.append(node.right)
        out.append(node.val)
    return out
