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
            k = parts[1]
            res = None
            for t in reversed(stack):
                if k in t:
                    res = t[k]
                    break
            if res is None:
                res = store.get(k, "NOT_FOUND")
            out.append(res)
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
                for t in stack:
                    store.update(t)
                stack.clear()
                out.append("OK")
    return out
