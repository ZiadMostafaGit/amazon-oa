# Simulation: permanent dict plus a stack of transaction dicts searched newest-first.
from typing import List, Optional, Any


def runDatabaseSimulator(operations: List[str]) -> List[str]:
    store = {}
    stack = []
    out = []
    for op in operations:
        parts = op.split()
        cmd = parts[0]
        if cmd == "BEGIN":
            stack.append({})
            out.append("OK")
        elif cmd == "SET":
            if not stack:
                out.append("ERROR")
            else:
                stack[-1][parts[1]] = parts[2]
                out.append("OK")
        elif cmd == "GET":
            key = parts[1]
            found = None
            for layer in reversed(stack):
                if key in layer:
                    found = layer[key]
                    break
            if found is None and key in store:
                found = store[key]
            out.append(found if found is not None else "NOT_FOUND")
        elif cmd == "COUNT":
            out.append(str(len(store)))
        elif cmd == "ROLLBACK":
            if not stack:
                out.append("ERROR")
            else:
                stack.pop()
                out.append("OK")
        elif cmd == "COMMIT":
            if not stack:
                out.append("ERROR")
            else:
                for layer in stack:
                    store.update(layer)
                stack = []
                out.append("OK")
    return out
