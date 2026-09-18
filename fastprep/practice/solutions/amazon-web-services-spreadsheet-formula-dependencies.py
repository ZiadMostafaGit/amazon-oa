# Store literals/formulas per cell; evaluate each GET with an iterative post-order DFS plus a memo invalidated on writes.
from typing import List, Optional, Any


def evaluateSpreadsheet(operations: List[str]) -> List[int]:
    literals = {}
    formulas = {}
    memo = {}
    out = []

    def value_of(cell: str) -> int:
        if cell in memo:
            return memo[cell]
        stack = [(cell, False)]
        while stack:
            name, expanded = stack.pop()
            if name in memo:
                continue
            terms = formulas.get(name)
            if terms is None:
                memo[name] = literals.get(name, 0)
                continue
            if not expanded:
                stack.append((name, True))
                for t in terms:
                    if not t[0].isdigit() and t[0] != '-' and t not in memo:
                        stack.append((t, False))
            else:
                total = 0
                for t in terms:
                    if t[0].isdigit() or t[0] == '-':
                        total += int(t)
                    else:
                        total += memo[t]
                memo[name] = total
        return memo[cell]

    for op in operations:
        parts = op.split()
        kind = parts[0]
        if kind == "SET":
            cell = parts[1]
            literals[cell] = int(parts[2])
            formulas.pop(cell, None)
            memo.clear()
        elif kind == "FORMULA":
            cell = parts[1]
            formulas[cell] = parts[2].split('+')
            literals.pop(cell, None)
            memo.clear()
        else:
            out.append(value_of(parts[1]))
    return out
