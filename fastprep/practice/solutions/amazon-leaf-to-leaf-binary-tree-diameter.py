# Post-order DFS returning max edges from node down to a leaf; combine only where both sides have leaves.
from typing import Optional, Any, Tuple


def leafToLeafDiameter(root: Optional['TreeNode']) -> int:
    best = -1

    # iterative post-order to avoid recursion depth limits on skewed trees
    if root is None:
        return 0

    depth = {}  # id(node) -> max edges from node down to a leaf in its subtree
    stack = [(root, False)]
    while stack:
        node, visited = stack.pop()
        if not visited:
            stack.append((node, True))
            if node.left is not None:
                stack.append((node.left, False))
            if node.right is not None:
                stack.append((node.right, False))
        else:
            if node.left is None and node.right is None:
                depth[id(node)] = 0
                continue
            if node.left is not None and node.right is not None:
                cand = depth[id(node.left)] + depth[id(node.right)] + 2
                if cand > best:
                    best = cand
                depth[id(node)] = max(depth[id(node.left)], depth[id(node.right)]) + 1
            elif node.left is not None:
                depth[id(node)] = depth[id(node.left)] + 1
            else:
                depth[id(node)] = depth[id(node.right)] + 1

    return best if best > 0 else 0
