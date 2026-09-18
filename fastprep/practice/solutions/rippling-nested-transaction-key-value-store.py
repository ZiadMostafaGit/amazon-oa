# Stack of transaction layers; each layer maps key -> value or a DELETED sentinel.
from typing import List, Optional, Any

_DELETED = object()


def processOperations(operations: List[List[str]]) -> List[str]:
    layers = [{}]  # layers[0] is the base store
    out = []
    for op in operations:
        cmd = op[0]
        if cmd == "SET":
            layers[-1][op[1]] = op[2]
        elif cmd == "DELETE":
            layers[-1][op[1]] = _DELETED
        elif cmd == "GET":
            key = op[1]
            value = "NULL"
            for i in range(len(layers) - 1, -1, -1):
                if key in layers[i]:
                    v = layers[i][key]
                    value = "NULL" if v is _DELETED else v
                    break
            out.append(value)
        elif cmd == "BEGIN":
            layers.append({})
        elif cmd == "COMMIT":
            top = layers.pop()
            layers[-1].update(top)
        elif cmd == "ROLLBACK":
            layers.pop()
    return out
