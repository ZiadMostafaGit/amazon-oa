# Approach: simulation with a file table (size, owner) plus per-user usage accounting and sorted eviction on capacity updates.
from typing import List

SUFFIX = ".COMPRESSED"


def cloudStorageCompression(operations: List[List[str]]) -> List[str]:
    files = {}          # name -> [size, owner or None for admin]
    capacity = {}       # user -> capacity
    used = {}           # user -> bytes used
    out = []

    def charge(owner, delta):
        if owner is not None:
            used[owner] = used.get(owner, 0) + delta

    def remaining(owner):
        return capacity[owner] - used.get(owner, 0)

    for op in operations:
        if not op:
            out.append("null")
            continue
        cmd = op[0]

        if cmd == "ADD_FILE":
            name, size = op[1], int(op[2])
            if name in files:
                out.append("false")
            else:
                files[name] = [size, None]
                out.append("true")

        elif cmd == "COPY_FILE":
            src, dst = op[1], op[2]
            if src not in files or dst in files:
                out.append("false")
            else:
                size, owner = files[src]
                files[dst] = [size, owner]
                charge(owner, size)
                out.append("true")

        elif cmd == "GET_FILE_SIZE":
            name = op[1]
            out.append(str(files[name][0]) if name in files else "null")

        elif cmd == "ADD_USER":
            uid, cap = op[1], int(op[2])
            if uid in capacity:
                out.append("false")
            else:
                capacity[uid] = cap
                used[uid] = 0
                out.append("true")

        elif cmd == "ADD_FILE_BY":
            uid, name, size = op[1], op[2], int(op[3])
            if uid not in capacity or name in files or size > remaining(uid):
                out.append("null")
            else:
                files[name] = [size, uid]
                charge(uid, size)
                out.append(str(remaining(uid)))

        elif cmd == "UPDATE_CAPACITY":
            uid, cap = op[1], int(op[2])
            if uid not in capacity:
                out.append("null")
            else:
                capacity[uid] = cap
                owned = [(n, s) for n, (s, o) in files.items() if o == uid]
                owned.sort(key=lambda x: (-x[1], x[0]))
                removed = 0
                i = 0
                while used.get(uid, 0) > cap and i < len(owned):
                    name, size = owned[i]
                    del files[name]
                    charge(uid, -size)
                    removed += 1
                    i += 1
                out.append(str(removed))

        elif cmd == "COMPRESS_FILE":
            uid, name = op[1], op[2]
            entry = files.get(name)
            target = name + SUFFIX
            if uid not in capacity or entry is None or entry[1] != uid or target in files:
                out.append("null")
            else:
                size = entry[0]
                del files[name]
                charge(uid, -size)
                new_size = size // 2
                files[target] = [new_size, uid]
                charge(uid, new_size)
                out.append(str(remaining(uid)))

        elif cmd == "DECOMPRESS_FILE":
            uid, name = op[1], op[2]
            entry = files.get(name)
            if (uid not in capacity or entry is None or entry[1] != uid
                    or not name.endswith(SUFFIX)):
                out.append("null")
            else:
                target = name[: -len(SUFFIX)]
                size = entry[0]
                new_size = size * 2
                if target in files or new_size - size > remaining(uid):
                    out.append("null")
                else:
                    del files[name]
                    charge(uid, -size)
                    files[target] = [new_size, uid]
                    charge(uid, new_size)
                    out.append(str(remaining(uid)))

        else:
            out.append("null")

    return out
