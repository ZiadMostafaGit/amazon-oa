# Trie where every node counts the stored occurrences passing through it; the root's count matches the empty prefix.
# Delete first checks the exact word is present (end count > 0), then decrements along its path.
from typing import List


class _Node:
    __slots__ = ("kids", "passing", "ending")

    def __init__(self):
        self.kids, self.passing, self.ending = {}, 0, 0


def solve(operations: List[str], values: List[str]) -> List[int]:
    root = _Node()
    out = []
    for op, s in zip(operations, values):
        if op == "insert":
            node = root
            node.passing += 1
            for ch in s:
                node = node.kids.setdefault(ch, _Node())
                node.passing += 1
            node.ending += 1
        elif op == "delete":
            path = [root]
            node = root
            for ch in s:
                node = node.kids.get(ch)
                if node is None:
                    break
                path.append(node)
            if node is None or node.ending == 0:
                continue
            node.ending -= 1
            for n in path:
                n.passing -= 1
        else:
            node = root
            for ch in s:
                node = node.kids.get(ch)
                if node is None:
                    break
            out.append(node.passing if node is not None else 0)
    return out
