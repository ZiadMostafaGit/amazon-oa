# Direct simulation with a dict, emitting one output line per GET/DELETE.
from typing import List


def runKeyValueStore(operations: List[List[str]]) -> List[str]:
    store = {}
    out = []
    for op in operations:
        kind = op[0]
        if kind == "SET":
            store[op[1]] = int(op[2])
        elif kind == "GET":
            key = op[1]
            if key in store:
                out.append("VALUE:" + str(store[key]))
            else:
                out.append("NULL")
        elif kind == "DELETE":
            if op[1] in store:
                del store[op[1]]
                out.append("true")
            else:
                out.append("false")
    return out
