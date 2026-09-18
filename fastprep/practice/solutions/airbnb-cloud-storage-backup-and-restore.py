# Direct simulation: dicts for files/owners/user capacities plus per-user backup snapshots.
from typing import List, Optional, Any


def processCloudStorage(operations: List[List[str]]) -> List[str]:
    ADMIN = "admin"
    files = {}          # name -> [size, owner]
    total_cap = {ADMIN: None}   # None means unlimited
    used = {ADMIN: 0}
    backups = {}        # user_id -> {name: size}
    out = []

    def user_exists(uid):
        return uid in total_cap

    def remaining(uid):
        return total_cap[uid] - used[uid]

    for op in operations:
        kind = op[0]

        if kind == "ADD_FILE":
            name, size = op[1], int(op[2])
            if name in files:
                out.append("false")
            else:
                files[name] = [size, ADMIN]
                used[ADMIN] += size
                out.append("true")

        elif kind == "GET_FILE_SIZE":
            name = op[1]
            out.append(str(files[name][0]) if name in files else "")

        elif kind == "DELETE_FILE":
            name = op[1]
            if name in files:
                size, owner = files.pop(name)
                used[owner] -= size
                out.append(str(size))
            else:
                out.append("")

        elif kind == "GET_N_LARGEST":
            prefix, n = op[1], int(op[2])
            matches = [(name, rec[0]) for name, rec in files.items() if name.startswith(prefix)]
            if not matches:
                out.append("")
            else:
                matches.sort(key=lambda p: (-p[1], p[0]))
                out.append(", ".join("%s(%d)" % (nm, sz) for nm, sz in matches[:n]))

        elif kind == "ADD_USER":
            uid, cap = op[1], int(op[2])
            if uid == ADMIN or user_exists(uid):
                out.append("false")
            else:
                total_cap[uid] = cap
                used[uid] = 0
                out.append("true")

        elif kind == "ADD_FILE_BY":
            uid, name, size = op[1], op[2], int(op[3])
            if uid == ADMIN or not user_exists(uid) or name in files or used[uid] + size > total_cap[uid]:
                out.append("")
            else:
                files[name] = [size, uid]
                used[uid] += size
                out.append(str(remaining(uid)))

        elif kind == "MERGE_USER":
            u1, u2 = op[1], op[2]
            if (u1 == u2 or u1 == ADMIN or u2 == ADMIN
                    or not user_exists(u1) or not user_exists(u2)):
                out.append("")
            else:
                for rec in files.values():
                    if rec[1] == u2:
                        rec[1] = u1
                total_cap[u1] += total_cap[u2]
                used[u1] += used[u2]
                del total_cap[u2]
                del used[u2]
                backups.pop(u2, None)
                out.append(str(remaining(u1)))

        elif kind == "BACKUP_USER":
            uid = op[1]
            if not user_exists(uid):
                out.append("")
            else:
                snap = {nm: rec[0] for nm, rec in files.items() if rec[1] == uid}
                backups[uid] = snap
                out.append(str(len(snap)))

        elif kind == "RESTORE_USER":
            uid = op[1]
            if not user_exists(uid):
                out.append("")
            else:
                for nm in [nm for nm, rec in files.items() if rec[1] == uid]:
                    del files[nm]
                used[uid] = 0
                snap = backups.get(uid)
                count = 0
                if snap:
                    for nm, sz in snap.items():
                        if nm in files:
                            continue
                        files[nm] = [sz, uid]
                        used[uid] += sz
                        count += 1
                out.append(str(count))

        else:
            out.append("")

    return out
