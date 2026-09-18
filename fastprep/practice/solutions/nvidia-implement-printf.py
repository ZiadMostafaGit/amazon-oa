# Single left-to-right scan of the pattern, emitting into a list and consuming values at each directive.
from typing import List, Optional, Any


def formatPrintf(pattern: str, values: List[str]) -> str:
    out = []
    vi = 0
    i = 0
    n = len(pattern)
    while i < n:
        ch = pattern[i]
        if ch == '%' and i + 1 < n:
            spec = pattern[i + 1]
            if spec == '%':
                out.append('%')
            elif spec == 's':
                out.append(values[vi])
                vi += 1
            elif spec == 'd':
                out.append(str(int(values[vi])))
                vi += 1
            else:
                out.append(ch)
                i += 1
                continue
            i += 2
            continue
        out.append(ch)
        i += 1
    return ''.join(out)
