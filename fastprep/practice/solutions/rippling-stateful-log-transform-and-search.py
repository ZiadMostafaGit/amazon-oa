# Simulation: apply each transform, append to an insertion-ordered store, and scan the store for searches.
from typing import List, Optional, Any


def _remove_all(log: str, target: str) -> str:
    # Delete non-overlapping literal occurrences left to right.
    if not target:
        return log
    out = []
    i = 0
    n = len(log)
    m = len(target)
    while i < n:
        if log.startswith(target, i):
            i += m
        else:
            out.append(log[i])
            i += 1
    return "".join(out)


def processLogs(operations: List[List[str]]) -> List[List[str]]:
    logs: List[str] = []
    result: List[List[str]] = []
    for op in operations:
        kind = op[0]
        if kind == "SEARCH":
            dedupe = op[1] == "true"
            keywords: List[str] = []
            seen = set()
            for kw in op[2:]:
                if kw not in seen:
                    seen.add(kw)
                    keywords.append(kw)
            row: List[str] = []
            for log in logs:
                if dedupe:
                    for kw in keywords:
                        if kw in log:
                            row.append(log)
                            break
                else:
                    for kw in keywords:
                        if kw in log:
                            row.append(log)
            result.append(row)
            continue
        if kind == "REMOVE":
            stored = _remove_all(op[1], op[2])
        elif kind == "TRUNCATE":
            stored = op[1][: int(op[2])]
        elif kind == "CAPITALIZE":
            stored = "".join(
                chr(ord(ch) - 32) if "a" <= ch <= "z" else ch for ch in op[1]
            )
        else:
            continue
        result.append([str(len(logs))])
        logs.append(stored)
    return result
