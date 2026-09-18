# Single live map plus a per-transaction undo log; commit splices the log into the parent.
from typing import List, Optional, Any


def runNestedKeyValueStore(commands: List[str]) -> List[str]:
    store = {}
    counts = {}
    undo_stack = []          # one list of (key, previous_value_or_None) per open transaction
    out = []

    def apply(key, value):
        old = store.get(key)
        if old is not None:
            c = counts[old] - 1
            if c:
                counts[old] = c
            else:
                del counts[old]
        if value is None:
            if key in store:
                del store[key]
        else:
            store[key] = value
            counts[value] = counts.get(value, 0) + 1
        return old

    def record(key, old):
        if undo_stack:
            undo_stack[-1].append((key, old))

    for cmd in commands:
        parts = cmd.split()
        op = parts[0]
        if op == "SET":
            key, value = parts[1], parts[2]
            old = apply(key, value)
            record(key, old)
            out.append("OK")
        elif op == "DELETE":
            key = parts[1]
            old = apply(key, None)
            record(key, old)
            out.append("OK")
        elif op == "GET":
            v = store.get(parts[1])
            out.append("NULL" if v is None else v)
        elif op == "COUNTVALUES":
            out.append(str(counts.get(parts[1], 0)))
        elif op == "BEGIN":
            undo_stack.append([])
            out.append("OK")
        elif op == "ROLLBACK":
            if not undo_stack:
                out.append("NO_TRANSACTION")
            else:
                log = undo_stack.pop()
                for key, old in reversed(log):
                    apply(key, old)
                out.append("OK")
        elif op == "COMMIT":
            if not undo_stack:
                out.append("NO_TRANSACTION")
            else:
                log = undo_stack.pop()
                if undo_stack:
                    undo_stack[-1].extend(log)
                out.append("OK")
        else:
            out.append("NULL")

    return out
