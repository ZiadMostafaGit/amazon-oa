# Hash map of accounts with Luhn card validation; simulate each command in order.
from typing import List, Optional, Any


def _luhn_valid(card: str) -> bool:
    if not (12 <= len(card) <= 16):
        return False
    if not card.isdigit():
        return False
    total = 0
    parity = len(card) % 2
    for i, ch in enumerate(card):
        d = ord(ch) - 48
        if i % 2 == parity:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def processCardCommands(operations: List[List[str]]) -> List[List[str]]:
    valid = {}
    limit = {}
    balance = {}
    for op in operations:
        kind = op[0]
        name = op[1]
        if kind == "Add":
            card = op[2]
            ok = _luhn_valid(card)
            valid[name] = ok
            balance[name] = 0
            limit[name] = int(op[3].lstrip("$")) if ok else 0
        elif kind == "Charge":
            if valid.get(name):
                amt = int(op[2].lstrip("$"))
                if balance[name] + amt <= limit[name]:
                    balance[name] += amt
        elif kind == "Credit":
            if valid.get(name):
                amt = int(op[2].lstrip("$"))
                balance[name] -= amt
    out = []
    for name in sorted(valid):
        if valid[name]:
            out.append([name, "$" + str(balance[name])])
        else:
            out.append([name, "error"])
    return out
