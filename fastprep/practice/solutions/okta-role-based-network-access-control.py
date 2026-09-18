# Simulation: maintain user->roles, role->permissions, permission->(effect, required props); a CHECK scans applicable permissions with DENY overriding ALLOW.
from typing import List, Dict, Set, Tuple


def evaluateAccess(operations: List[List[str]]) -> List[str]:
    users: Dict[str, Set[str]] = {}
    roles: Dict[str, Set[str]] = {}
    perms: Dict[str, Tuple[str, Dict[str, str]]] = {}
    out: List[str] = []

    for row in operations:
        op = row[0]
        if op == "CREATE_USER":
            users.setdefault(row[1], set())
        elif op == "CREATE_ROLE":
            roles.setdefault(row[1], set())
        elif op == "CREATE_PERMISSION":
            pid = row[1]
            effect = row[2]
            k = int(row[3])
            props: Dict[str, str] = {}
            for i in range(k):
                props[row[4 + 2 * i]] = row[5 + 2 * i]
            perms[pid] = (effect, props)
        elif op == "ASSIGN_PERMISSION":
            rid, pid = row[1], row[2]
            if rid not in roles or pid not in perms:
                out.append("ERROR")
            else:
                roles[rid].add(pid)
        elif op == "ASSIGN_ROLE":
            uid, rid = row[1], row[2]
            if uid not in users or rid not in roles:
                out.append("ERROR")
            else:
                users[uid].add(rid)
        elif op == "CHECK":
            uid = row[1]
            if uid not in users:
                out.append("ERROR")
                continue
            k = int(row[2])
            ctx: Dict[str, str] = {}
            for i in range(k):
                ctx[row[3 + 2 * i]] = row[4 + 2 * i]
            decision = "DENY"
            seen: Set[str] = set()
            denied = False
            allowed = False
            for rid in users[uid]:
                for pid in roles.get(rid, ()):
                    if pid in seen:
                        continue
                    seen.add(pid)
                    effect, props = perms[pid]
                    ok = True
                    for key, val in props.items():
                        if ctx.get(key) != val:
                            ok = False
                            break
                    if not ok:
                        continue
                    if effect == "DENY":
                        denied = True
                        break
                    allowed = True
                if denied:
                    break
            if denied:
                decision = "DENY"
            elif allowed:
                decision = "ALLOW"
            out.append(decision)
    return out
