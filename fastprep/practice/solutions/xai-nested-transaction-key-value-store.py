# Single live map plus per-transaction undo logs; commit splices the child log into its parent.
from typing import List


def runNestedTransactions(operations: List[List[str]]) -> List[str]:
    store = {}
    logs = []  # stack of undo logs: list of (key, had_old, old_value)
    out = []
    for op in operations:
        kind = op[0]
        if kind == "SET":
            key, value = op[1], op[2]
            if logs:
                if key in store:
                    logs[-1].append((key, True, store[key]))
                else:
                    logs[-1].append((key, False, None))
            store[key] = value
        elif kind == "GET":
            out.append(store.get(op[1], "NULL"))
        elif kind == "BEGIN":
            logs.append([])
        elif kind == "COMMIT":
            child = logs.pop()
            if logs:
                logs[-1].extend(child)
        elif kind == "ROLLBACK":
            child = logs.pop()
            for key, had_old, old_value in reversed(child):
                if had_old:
                    store[key] = old_value
                else:
                    store.pop(key, None)
    return out
