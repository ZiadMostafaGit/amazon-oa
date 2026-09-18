# Iterative left-first DFS carrying running sums, keeping the first minimum leaf and
# rebuilding its path from a parent map.
from typing import List, Optional, Any


def minimumSumRootToLeafPath(root: Optional[TreeNode]) -> List[int]:
    if root is None:
        return []
    parent = {id(root): None}
    best_leaf = None
    best_sum = None
    stack = [(root, root.val)]
    while stack:
        node, total = stack.pop()
        if node.left is None and node.right is None:
            if best_sum is None or total < best_sum:
                best_sum = total
                best_leaf = node
            continue
        for child in (node.right, node.left):
            if child is not None:
                parent[id(child)] = node
                stack.append((child, total + child.val))

    path = []
    cur = best_leaf
    while cur is not None:
        path.append(cur.val)
        cur = parent[id(cur)]
    path.reverse()
    return path
