# Approach: nested hash maps employee -> resource -> set of access types, with fixed READ/WRITE/ADMIN ordering.
from typing import List

ORDER = ["READ", "WRITE", "ADMIN"]


def manageEmployeeAccess(operations: List[List[str]]) -> List[List[str]]:
    store = {}
    results = []
    for op in operations:
        if not op:
            results.append([])
            continue
        action = op[0]
        if action == "GRANT":
            emp, res, acc = op[1], op[2], op[3]
            bucket = store.setdefault(emp, {}).setdefault(res, set())
            if acc in bucket:
                results.append(["false"])
            else:
                bucket.add(acc)
                results.append(["true"])
        elif action == "REVOKE":
            emp, res, acc = op[1], op[2], op[3]
            bucket = store.get(emp, {}).get(res)
            removed = False
            if bucket:
                if acc == "ALL":
                    removed = True
                    bucket.clear()
                elif acc in bucket:
                    bucket.discard(acc)
                    removed = True
                if not bucket:
                    store[emp].pop(res, None)
            results.append(["true"] if removed else ["false"])
        elif action == "GET_ACCESS":
            emp, res = op[1], op[2]
            bucket = store.get(emp, {}).get(res, set())
            results.append([a for a in ORDER if a in bucket])
        elif action == "GET_RESOURCES":
            emp = op[1]
            resources = [r for r, v in store.get(emp, {}).items() if v]
            resources.sort()
            results.append(resources)
        else:
            results.append([])
    return results
