# Dependency-graph spreadsheet: SET does a reachability cycle check, GET does an iterative DFS evaluation.
from typing import List, Optional, Any
import re

_LINE = re.compile(r'^\s*(SET|GET)\s+([A-Za-z]\d+)\s*(.*)$')


def _parse_expr(expr: str):
    expr = expr.strip()
    if expr.startswith('='):
        expr = expr[1:]
    terms = []
    for part in expr.split('+'):
        p = part.strip()
        if not p:
            continue
        if p.isdigit():
            terms.append(int(p))
        else:
            terms.append(p.upper())
    return terms


def solveSpreadsheetFormulaEvaluator(input: str) -> List[str]:
    cells = {}
    out = []

    def creates_cycle(target, terms):
        stack = [t for t in terms if isinstance(t, str)]
        seen = set()
        while stack:
            c = stack.pop()
            if c == target:
                return True
            if c in seen:
                continue
            seen.add(c)
            for t in cells.get(c, ()):
                if isinstance(t, str):
                    stack.append(t)
        return False

    def evaluate(start):
        if start not in cells:
            return None
        memo = {}
        stack = [(start, False)]
        while stack:
            c, expanded = stack.pop()
            if c in memo:
                continue
            terms = cells.get(c)
            if terms is None:
                return None
            if not expanded:
                stack.append((c, True))
                for t in terms:
                    if isinstance(t, str) and t not in memo:
                        if t not in cells:
                            return None
                        stack.append((t, False))
            else:
                total = 0
                for t in terms:
                    total += t if isinstance(t, int) else memo[t]
                memo[c] = total
        return memo[start]

    for raw in input.split('\n'):
        if not raw.strip():
            continue
        m = _LINE.match(raw)
        if not m:
            out.append("ERROR")
            continue
        cmd, cell, rest = m.group(1), m.group(2).upper(), m.group(3)
        if cmd == "SET":
            terms = _parse_expr(rest)
            if creates_cycle(cell, terms):
                out.append("ERROR")
            else:
                cells[cell] = terms
                out.append("OK")
        else:
            val = evaluate(cell)
            out.append("ERROR" if val is None else str(val))
    return out
