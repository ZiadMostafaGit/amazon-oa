# Iterative DFS (left before right) carrying the running sum and the current path.
from typing import List, Optional, Any


def pathSum(root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
    res = []
    if root is None:
        return res
    path = []

    def dfs(node, remaining):
        path.append(node.val)
        remaining -= node.val
        if node.left is None and node.right is None:
            if remaining == 0:
                res.append(list(path))
        else:
            if node.left is not None:
                dfs(node.left, remaining)
            if node.right is not None:
                dfs(node.right, remaining)
        path.pop()

    import sys
    sys.setrecursionlimit(20000)
    dfs(root, targetSum)
    return res
