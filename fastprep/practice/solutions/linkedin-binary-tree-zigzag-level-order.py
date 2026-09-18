# BFS level-order traversal, reversing every other level's values.
from typing import List, Optional, Any


def zigzagLevelOrder(root: Optional["TreeNode"]) -> List[List[int]]:
    if root is None:
        return []
    result = []
    level = [root]
    left_to_right = True
    while level:
        vals = [node.val for node in level]
        if not left_to_right:
            vals.reverse()
        result.append(vals)
        nxt = []
        for node in level:
            if node.left is not None:
                nxt.append(node.left)
            if node.right is not None:
                nxt.append(node.right)
        level = nxt
        left_to_right = not left_to_right
    return result
