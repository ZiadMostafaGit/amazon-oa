# Build a binary trie of the codes; walk it bit by bit, emitting at each leaf.
from typing import List, Optional, Any


def decode(codes: List[str], encoded: str) -> str:
    root = {}
    for line in codes:
        ch, _, code = line.partition("\t")
        if ch == "[newline]":
            ch = "\n"
        node = root
        for b in code.strip():
            node = node.setdefault(b, {})
        node["$"] = ch
    out = []
    node = root
    for b in encoded:
        node = node[b]
        if "$" in node:
            out.append(node["$"])
            node = root
    return "".join(out)
