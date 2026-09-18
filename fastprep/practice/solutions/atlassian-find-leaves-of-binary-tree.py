# Group nodes by their height above the tree's leaves via an iterative postorder traversal.
from typing import List, Optional, Any


def findLeaves(root: Optional[TreeNode]) -> List[List[int]]:
    layers: List[List[int]] = []
    heights = {}

    stack = [(root, False)]
    while stack:
        node, processed = stack.pop()
        if node is None:
            continue
        if not processed:
            stack.append((node, True))
            stack.append((node.right, False))
            stack.append((node.left, False))
            continue
        lh = heights.get(id(node.left), -1) if node.left is not None else -1
        rh = heights.get(id(node.right), -1) if node.right is not None else -1
        h = max(lh, rh) + 1
        heights[id(node)] = h
        if h == len(layers):
            layers.append([])
        layers[h].append(node.val)
    return layers
