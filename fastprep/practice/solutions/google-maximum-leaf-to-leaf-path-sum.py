# Post-order: down[v] = best sum of a path from v down to a leaf (it must end at a real leaf, so a node with one
# child can only continue into that child). A node with two children joins its two best downward paths.
from typing import Optional, Any


def maxLeafToLeafPathSum(root: Optional["TreeNode"]) -> int:
    best = None
    down = {}
    stack = [(root, False)]
    while stack:
        node, done = stack.pop()
        if not done:
            stack.append((node, True))
            if node.left is not None:
                stack.append((node.left, False))
            if node.right is not None:
                stack.append((node.right, False))
            continue
        l, r = node.left, node.right
        if l is None and r is None:
            down[node] = node.val
        elif l is None:
            down[node] = node.val + down[r]
        elif r is None:
            down[node] = node.val + down[l]
        else:
            through = down[l] + down[r] + node.val
            if best is None or through > best:
                best = through
            down[node] = node.val + max(down[l], down[r])
    return best
