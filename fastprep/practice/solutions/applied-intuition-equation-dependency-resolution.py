# Parse each definition, detect cycles among defined variables with an iterative DFS, then evaluate in topological order.
from typing import List, Optional, Any


def _parse(eq: str):
    lhs, rhs = eq.split("=", 1)
    name = lhs.strip()
    terms = [t.strip() for t in rhs.split("+")]
    return name, terms


def _is_int(tok: str) -> bool:
    if not tok:
        return False
    body = tok[1:] if tok[0] in "+-" else tok
    return body.isdigit()


def resolveEquations(equations: List[str]) -> List[str]:
    names = []
    terms_of = {}
    for eq in equations:
        name, terms = _parse(eq)
        names.append(name)
        terms_of[name] = terms

    defined = set(names)

    # cycle detection over edges between defined variables (cycles take precedence)
    WHITE, GREY, BLACK = 0, 1, 2
    color = {n: WHITE for n in names}
    for root in names:
        if color[root] != WHITE:
            continue
        stack = [(root, 0)]
        color[root] = GREY
        while stack:
            node, idx = stack.pop()
            deps = [t for t in terms_of[node] if not _is_int(t) and t in defined]
            if idx < len(deps):
                stack.append((node, idx + 1))
                nxt = deps[idx]
                if color[nxt] == GREY:
                    return ["Cyclic Dependency"]
                if color[nxt] == WHITE:
                    color[nxt] = GREY
                    stack.append((nxt, 0))
            else:
                color[node] = BLACK

    # undefined references
    for name in names:
        for t in terms_of[name]:
            if not _is_int(t) and t not in defined:
                return ["Unresolvable equations"]

    value = {}

    def resolve(start: str) -> int:
        if start in value:
            return value[start]
        stack = [start]
        while stack:
            node = stack[-1]
            if node in value:
                stack.pop()
                continue
            pending = [t for t in terms_of[node] if not _is_int(t) and t not in value]
            if pending:
                stack.extend(pending)
                continue
            total = 0
            for t in terms_of[node]:
                total += int(t) if _is_int(t) else value[t]
            value[node] = total
            stack.pop()
        return value[start]

    return ["%s=%d" % (n, resolve(n)) for n in names]
