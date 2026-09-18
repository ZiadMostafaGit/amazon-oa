# Greedy bottom-up DFS: 0 = needs cover, 1 = covered without camera, 2 = has camera.
from typing import Optional, Any


def solve(root: Optional["TreeNode"]) -> int:
    count = 0

    def dfs(node):
        nonlocal count
        if node is None:
            return 1
        left = dfs(node.left)
        right = dfs(node.right)
        if left == 0 or right == 0:
            count += 1
            return 2
        if left == 2 or right == 2:
            return 1
        return 0

    if dfs(root) == 0:
        count += 1
    return count
