# Parse pairs, validate error codes in priority order, then emit the S-expression iteratively.
import re
from typing import List, Optional, Any

_TOKEN = re.compile(r"^\([A-Z],[A-Z]\)$")


def validateBinaryTree(pairs: str) -> str:
    text = pairs.strip() if pairs is not None else ""
    if not text:
        return "E1"
    tokens = text.split(" ")
    parsed = []
    for tok in tokens:
        if not _TOKEN.match(tok):
            return "E1"
        parsed.append((tok[1], tok[3]))

    seen = set()
    children = {}
    parent = {}
    nodes = set()
    dup = False
    too_many = False
    for p, c in parsed:
        nodes.add(p)
        nodes.add(c)
        if (p, c) in seen:
            dup = True
            continue
        seen.add((p, c))
        kids = children.setdefault(p, [])
        if len(kids) == 2:
            too_many = True
        else:
            kids.append(c)
        parent.setdefault(c, p)
    if dup:
        return "E2"
    if too_many:
        return "E3"

    roots = [n for n in nodes if n not in parent]
    if len(roots) > 1:
        return "E4"
    if not roots:
        return "E5"
    root = roots[0]

    for kids in children.values():
        kids.sort()

    # Iterative post-order assembly of the S-expression.
    parts = {}
    stack = [(root, False)]
    visited = set()
    while stack:
        node, expanded = stack.pop()
        if expanded:
            body = "".join(parts[k] for k in children.get(node, ()))
            parts[node] = "(" + node + body + ")"
            continue
        if node in visited:
            return "E5"
        visited.add(node)
        stack.append((node, True))
        for k in children.get(node, ()):
            stack.append((k, False))
    if len(visited) != len(nodes):
        return "E5"
    return parts[root]
