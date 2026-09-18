# Iterative postorder computing each node's height; height indexes the removal round.
from typing import List, Optional, Any


def findLeaves(root: Optional[TreeNode]) -> List[List[int]]:
    layers: List[List[int]] = []
    if root is None:
        return layers
    height = {}
    stack = [(root, False)]
    while stack:
        node, expanded = stack.pop()
        if expanded:
            lh = height.get(id(node.left), -1) if node.left else -1
            rh = height.get(id(node.right), -1) if node.right else -1
            h = max(lh, rh) + 1
            height[id(node)] = h
            while len(layers) <= h:
                layers.append([])
            layers[h].append(node.val)
        else:
            stack.append((node, True))
            if node.right:
                stack.append((node.right, False))
            if node.left:
                stack.append((node.left, False))
    return layers
