# Iterative BFS collecting one list per level.
from typing import List, Optional, Any


def levelOrder(root: Optional[TreeNode]) -> List[List[int]]:
    if root is None:
        return []
    res: List[List[int]] = []
    level = [root]
    while level:
        res.append([node.val for node in level])
        nxt = []
        for node in level:
            if node.left is not None:
                nxt.append(node.left)
            if node.right is not None:
                nxt.append(node.right)
        level = nxt
    return res
