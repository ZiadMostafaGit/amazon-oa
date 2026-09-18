# Hash map of cell -> raw text; computed view parses "=a+b" on demand.
from typing import List, Optional, Any


def _computed(raw: str) -> str:
    if raw == "":
        return ""
    if raw[0] == "=":
        body = raw[1:]
        split = -1
        for i in range(1, len(body)):
            if body[i] == "+" and body[i - 1].isdigit():
                split = i
                break
        if split == -1:
            return str(int(body))
        return str(int(body[:split]) + int(body[split + 1:]))
    return str(int(raw))


def runSpreadsheet(operations: List[List[str]]) -> List[str]:
    cells = {}
    out = []
    for op in operations:
        kind = op[0]
        if kind == "SET":
            cell, value = op[1], op[2]
            if value == "":
                cells.pop(cell, None)
            else:
                cells[cell] = value
        elif kind == "GET_RAW":
            out.append(cells.get(op[1], ""))
        else:
            out.append(_computed(cells.get(op[1], "")))
    return out
