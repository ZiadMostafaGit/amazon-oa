# Simulation: a committed dict plus an optional overlay dict for the single active transaction.
from typing import List, Optional, Any


def processTransactions(operations: List[List[str]]) -> List[str]:
    committed = {}
    overlay = None
    out = []

    for op in operations:
        cmd = op[0]
        if cmd == "SET":
            key, value = op[1], op[2]
            if overlay is not None:
                overlay[key] = value
            else:
                committed[key] = value
        elif cmd == "GET":
            key = op[1]
            if overlay is not None and key in overlay:
                out.append(overlay[key])
            elif key in committed:
                out.append(committed[key])
            else:
                out.append("null")
        elif cmd == "BEGIN":
            overlay = {}
        elif cmd == "COMMIT":
            if overlay is not None:
                committed.update(overlay)
                overlay = None
                out.append("true")
            else:
                out.append("false")
        elif cmd == "ROLLBACK":
            if overlay is not None:
                overlay = None
                out.append("true")
            else:
                out.append("false")
    return out
