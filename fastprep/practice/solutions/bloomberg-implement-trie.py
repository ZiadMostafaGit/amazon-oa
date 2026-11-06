# A trie of nested dicts; a sentinel key marks the end of a complete word.
from typing import List

_END = "$"


def trieOperations(operations: List[str], values: List[str]) -> List[bool]:
    root = {}
    out = []
    for op, word in zip(operations, values):
        if op == "insert":
            node = root
            for ch in word:
                node = node.setdefault(ch, {})
            node[_END] = True
            continue
        node = root
        for ch in word:
            node = node.get(ch)
            if node is None:
                break
        if node is None:
            out.append(False)
        elif op == "search":
            out.append(_END in node)
        else:
            out.append(True)
    return out
