# Recursive expansion with memoization and an on-stack set to detect cycles or missing keys.
from typing import List, Optional, Any


class _Fail(Exception):
    pass


def expandTemplate(mappings: List[List[str]], source: str) -> str:
    table = {}
    for pair in mappings:
        table[pair[0]] = pair[1]

    resolved = {}
    on_stack = set()

    def expand(text: str) -> str:
        out = []
        i = 0
        n = len(text)
        while i < n:
            ch = text[i]
            if ch == '%':
                end = text.find('%', i + 1)
                if end == -1:
                    raise _Fail()
                key = text[i + 1:end]
                if key == "":
                    out.append('%')
                else:
                    out.append(resolve(key))
                i = end + 1
            else:
                out.append(ch)
                i += 1
        return "".join(out)

    def resolve(key: str) -> str:
        if key in resolved:
            return resolved[key]
        if key in on_stack:
            raise _Fail()
        if key not in table:
            raise _Fail()
        on_stack.add(key)
        value = expand(table[key])
        on_stack.discard(key)
        resolved[key] = value
        return value

    try:
        return expand(source)
    except _Fail:
        return "ERROR"
