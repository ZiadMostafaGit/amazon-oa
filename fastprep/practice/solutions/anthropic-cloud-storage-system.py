# Direct simulation: hash maps for files/owners/users plus per-user backup snapshots.
from typing import List, Optional, Any

ADMIN = "admin"
UNLIMITED = 10 ** 18


def cloudStorageSystem(operations: List[List[str]]) -> List[List[str]]:
    files = {}                       # name -> [size, owner]
    users = {ADMIN: {"cap": UNLIMITED, "used": 0, "files": set(), "backup": None}}
    out = []

    def rem(uid):
        u = users[uid]
        return u["cap"] - u["used"]

    def drop(name):
        size, owner = files.pop(name)
        u = users.get(owner)
        if u is not None:
            u["files"].discard(name)
            u["used"] -= size
        return size

    def put(name, size, owner):
        files[name] = [size, owner]
        u = users[owner]
        u["files"].add(name)
        u["used"] += size

    for op in operations:
        kind = op[0]

        if kind == "ADD_FILE":
            name, size = op[1], int(op[2])
            if name in files:
                out.append(["false"])
            else:
                put(name, size, ADMIN)
                out.append(["true"])

        elif kind == "GET_FILE_SIZE":
            name = op[1]
            out.append([str(files[name][0])] if name in files else [])

        elif kind == "DELETE_FILE":
            name = op[1]
            out.append([str(drop(name))] if name in files else [])

        elif kind == "GET_N_LARGEST":
            prefix, n = op[1], int(op[2])
            matches = [(nm, sz) for nm, (sz, _o) in files.items() if nm.startswith(prefix)]
            matches.sort(key=lambda t: (-t[1], t[0]))
            out.append(["%s(%d)" % (nm, sz) for nm, sz in matches[:n]] if n > 0 else [])

        elif kind == "ADD_USER":
            uid, cap = op[1], int(op[2])
            if uid in users:
                out.append(["false"])
            else:
                users[uid] = {"cap": cap, "used": 0, "files": set(), "backup": None}
                out.append(["true"])

        elif kind == "ADD_FILE_BY":
            uid, name, size = op[1], op[2], int(op[3])
            if uid not in users or name in files or users[uid]["used"] + size > users[uid]["cap"]:
                out.append([])
            else:
                put(name, size, uid)
                out.append([str(rem(uid))])

        elif kind == "MERGE_USER":
            a, b = op[1], op[2]
            if a == b or a not in users or b not in users:
                out.append([])
            else:
                for name in list(users[b]["files"]):
                    size = files[name][0]
                    files[name][1] = a
                    users[a]["files"].add(name)
                    users[a]["used"] += size
                users[a]["cap"] += users[b]["cap"]
                del users[b]
                out.append([str(rem(a))])

        elif kind == "BACKUP_USER":
            uid = op[1]
            if uid not in users:
                out.append([])
            else:
                snap = {name: files[name][0] for name in users[uid]["files"]}
                users[uid]["backup"] = snap
                out.append([str(len(snap))])

        elif kind == "RESTORE_USER":
            uid = op[1]
            if uid not in users:
                out.append([])
            else:
                for name in list(users[uid]["files"]):
                    drop(name)
                snap = users[uid]["backup"]
                count = 0
                if snap:
                    for name in sorted(snap):
                        if name not in files:
                            put(name, snap[name], uid)
                            count += 1
                out.append([str(count)])

        else:
            out.append([])

    return out
