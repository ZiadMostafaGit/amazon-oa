# Straightforward rule parsing and short-circuit evaluation in insertion order.
from typing import List, Optional, Any


def _parse_value(tok: str):
    tok = tok.strip()
    if tok == "true":
        return True
    if tok == "false":
        return False
    return int(tok)


def _split_atom(atom: str):
    atom = atom.strip()
    for op in (">=", "<=", "!=", "=", ">", "<"):
        i = atom.find(op)
        if i > 0:
            return atom[:i].strip(), op, atom[i + len(op):].strip()
    return None


def _eval_atom(atom: str, attrs) -> bool:
    field, op, lit = _split_atom(atom)
    left = attrs.get(field)
    right = _parse_value(lit)
    if op == "=":
        return type(left) is type(right) and left == right
    if op == "!=":
        return not (type(left) is type(right) and left == right)
    if isinstance(left, bool) or isinstance(right, bool):
        return False
    if op == ">":
        return left > right
    if op == ">=":
        return left >= right
    if op == "<":
        return left < right
    return left <= right


def evaluateOrderedRules(rules: List[str], attributes: List[str]) -> str:
    attrs = {}
    for a in attributes:
        k, _, v = a.partition("=")
        attrs[k.strip()] = _parse_value(v)

    for rule in rules:
        r = rule.strip()
        action, _, cond = r.partition(" if ")
        action = action.strip()
        cond = cond.strip()
        if " AND " in cond:
            ok = all(_eval_atom(p, attrs) for p in cond.split(" AND "))
        elif " OR " in cond:
            ok = any(_eval_atom(p, attrs) for p in cond.split(" OR "))
        else:
            ok = _eval_atom(cond, attrs)
        if ok:
            return action
    return "REVIEW"
