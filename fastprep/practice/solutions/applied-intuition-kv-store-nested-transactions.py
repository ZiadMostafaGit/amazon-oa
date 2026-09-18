# Single dict plus a stack of per-transaction undo logs (old value or sentinel) for O(1) amortized ops.
from typing import List, Optional, Any

_MISSING = object()


def runNestedTransactions(commands: List[str]) -> List[str]:
    store = {}
    undo_stack = []  # one list of (key, previous_value) per open transaction
    out = []

    for line in commands:
        parts = line.split()
        if not parts:
            continue
        op = parts[0].upper()

        if op == "SET" and len(parts) >= 3:
            key, value = parts[1], parts[2]
            if undo_stack:
                undo_stack[-1].append((key, store.get(key, _MISSING)))
            store[key] = value
        elif op == "GET" and len(parts) >= 2:
            out.append(store.get(parts[1], "NULL"))
        elif op == "DELETE" and len(parts) >= 2:
            key = parts[1]
            if undo_stack:
                undo_stack[-1].append((key, store.get(key, _MISSING)))
            store.pop(key, None)
        elif op == "BEGIN":
            undo_stack.append([])
        elif op == "ROLLBACK":
            if not undo_stack:
                out.append("NO TRANSACTION")
            else:
                log = undo_stack.pop()
                for key, prev in reversed(log):
                    if prev is _MISSING:
                        store.pop(key, None)
                    else:
                        store[key] = prev
        elif op == "COMMIT":
            if not undo_stack:
                out.append("NO TRANSACTION")
            else:
                log = undo_stack.pop()
                if undo_stack:
                    undo_stack[-1].extend(log)

    return out
