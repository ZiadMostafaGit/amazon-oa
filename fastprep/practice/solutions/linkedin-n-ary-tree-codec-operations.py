# Iterative stack-based parsers/emitters for both the parenthesized tree text and the preorder value:childCount wire format.
from typing import List, Optional, Any


class _Node:
    __slots__ = ("val", "children")

    def __init__(self, val: int):
        self.val = val
        self.children = []


def _parse_text(s: str) -> _Node:
    stack = []
    root = None
    last = None
    i, L = 0, len(s)
    while i < L:
        c = s[i]
        if c.isdigit():
            j = i
            while j < L and s[j].isdigit():
                j += 1
            node = _Node(int(s[i:j]))
            if stack:
                stack[-1].children.append(node)
            else:
                root = node
            last = node
            i = j
        elif c == "(":
            stack.append(last)
            i += 1
        elif c == ",":
            i += 1
        else:  # ')'
            last = stack.pop()
            i += 1
    return root


def _emit_wire(root: _Node) -> str:
    parts = []
    stack = [root]
    while stack:
        node = stack.pop()
        parts.append(str(node.val) + ":" + str(len(node.children)))
        if node.children:
            stack.extend(reversed(node.children))
    return "|".join(parts)


def _parse_wire(s: str) -> _Node:
    tokens = s.split("|")
    root = None
    stack = []
    for tok in tokens:
        v, _, c = tok.partition(":")
        node = _Node(int(v))
        cnt = int(c)
        if root is None:
            root = node
        else:
            frame = stack[-1]
            frame[0].children.append(node)
            frame[1] -= 1
        if cnt > 0:
            stack.append([node, cnt])
        else:
            while stack and stack[-1][1] == 0:
                stack.pop()
    return root


def _emit_text(root: _Node) -> str:
    out = [str(root.val)]
    if root.children:
        out.append("(")
    stack = [[root, 0]]
    while stack:
        frame = stack[-1]
        node, idx = frame[0], frame[1]
        if idx < len(node.children):
            frame[1] += 1
            if idx > 0:
                out.append(",")
            child = node.children[idx]
            out.append(str(child.val))
            if child.children:
                out.append("(")
                stack.append([child, 0])
        else:
            stack.pop()
            if node.children:
                out.append(")")
    return "".join(out)


def transformNaryCodec(operations: List[List[str]]) -> List[str]:
    results = []
    for op in operations:
        kind, payload = op[0], op[1]
        if kind == "SERIALIZE":
            results.append(_emit_wire(_parse_text(payload)))
        else:
            results.append(_emit_text(_parse_wire(payload)))
    return results
