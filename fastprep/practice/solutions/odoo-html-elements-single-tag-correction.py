# Tokenize tags, stack-check nesting; if broken, brute-force one-name edits in token order.
import re

ALLOWED = ("b", "i", "em", "div", "p")
_TAG = re.compile(r"</?(b|i|em|div|p)>")


def _nested(tokens) -> bool:
    stack = []
    for name, is_open in tokens:
        if is_open:
            stack.append(name)
        else:
            if not stack or stack[-1] != name:
                return False
            stack.pop()
    return not stack


def htmlElements(str: str) -> str:
    tokens = []
    for m in _TAG.finditer(str):
        tokens.append((m.group(1), not m.group(0).startswith("</")))

    if _nested(tokens):
        return "true"

    for i, (name, is_open) in enumerate(tokens):
        for alt in ALLOWED:
            if alt == name:
                continue
            tokens[i] = (alt, is_open)
            if _nested(tokens):
                tokens[i] = (name, is_open)
                return name
        tokens[i] = (name, is_open)
    return "true"
