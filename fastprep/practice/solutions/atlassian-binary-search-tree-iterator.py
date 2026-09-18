# Controlled-recursion BST iterator using an explicit stack of leftmost spines.
from typing import List, Optional, Any


class _BSTIterator:
    def __init__(self, root):
        self.stack = []
        self._push_left(root)

    def _push_left(self, node):
        while node is not None:
            self.stack.append(node)
            node = node.left

    def hasNext(self) -> bool:
        return len(self.stack) > 0

    def next(self) -> int:
        node = self.stack.pop()
        if node.right is not None:
            self._push_left(node.right)
        return node.val


def runBSTIterator(root: Optional[TreeNode], operations: List[str]) -> List[str]:
    it = _BSTIterator(root)
    out: List[str] = []
    for op in operations:
        if op == "next":
            out.append(str(it.next()))
        elif op == "hasNext":
            out.append("true" if it.hasNext() else "false")
    return out
