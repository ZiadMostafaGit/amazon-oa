# Postorder DFS returning (is_bst, min, max, sum) per subtree and tracking the best BST sum.
from __future__ import annotations

from typing import Optional, Any


def solve(root: Optional["TreeNode"]) -> int:
    best = 0

    def dfs(node):
        # returns (is_bst, min_val, max_val, total)
        nonlocal best
        if node is None:
            return True, float('inf'), float('-inf'), 0
        l_ok, l_min, l_max, l_sum = dfs(node.left)
        r_ok, r_min, r_max, r_sum = dfs(node.right)
        if l_ok and r_ok and l_max < node.val < r_min:
            total = l_sum + r_sum + node.val
            if total > best:
                best = total
            return True, min(l_min, node.val), max(r_max, node.val), total
        return False, float('-inf'), float('inf'), 0

    dfs(root)
    return best
