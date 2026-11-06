# Trie insert; find walks the trie, and a '.' branches into every child (DFS over the trie).
from typing import List

_END = "$"


def solve(operations: List[List[str]]) -> List[bool]:
    root = {}
    out = []

    def find(node, pattern, i):
        if i == len(pattern):
            return _END in node
        ch = pattern[i]
        if ch == ".":
            for key, child in node.items():
                if key != _END and find(child, pattern, i + 1):
                    return True
            return False
        child = node.get(ch)
        return child is not None and find(child, pattern, i + 1)

    for op, word in operations:
        if op == "insert":
            node = root
            for ch in word:
                node = node.setdefault(ch, {})
            node[_END] = True
        else:
            out.append(find(root, word, 0))
    return out
