# Simulate a hash-map record store, emitting OK / ERROR / value per command.
from typing import List, Optional, Any


def recordStore(operations: List[str]) -> List[str]:
    store = {}
    results: List[str] = []
    for op in operations:
        parts = op.split()
        cmd = parts[0]
        key = parts[1]
        if cmd == "INSERT":
            if key in store:
                results.append("ERROR")
            else:
                store[key] = parts[2]
                results.append("OK")
        elif cmd == "UPDATE":
            if key in store:
                store[key] = parts[2]
                results.append("OK")
            else:
                results.append("ERROR")
        elif cmd == "REMOVE":
            if key in store:
                del store[key]
                results.append("OK")
            else:
                results.append("ERROR")
        else:
            results.append(store[key] if key in store else "ERROR")
    return results
