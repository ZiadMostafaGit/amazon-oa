# DFS backtracking over root-to-leaf paths, collecting those whose values sum to targetSum.
from typing import List, Optional, Any


def solve(root: Optional["TreeNode"], targetSum: int) -> List[List[int]]:
    res: List[List[int]] = []
    path: List[int] = []

    def dfs(node, remaining):
        if node is None:
            return
        path.append(node.val)
        remaining -= node.val
        if node.left is None and node.right is None:
            if remaining == 0:
                res.append(list(path))
        else:
            dfs(node.left, remaining)
            dfs(node.right, remaining)
        path.pop()

    dfs(root, targetSum)
    return res
