# Simulation: dict of path -> file record plus per-user usage, with all-or-nothing validation per op.
from typing import List, Optional, Any

SUFFIX = ".COMPRESSED"


def processFileSystem(operations: List[List[str]]) -> List[str]:
    # user id -> capacity (None means unlimited)
    capacity = {"admin": None}
    usage = {"admin": 0}
    # path -> [owner, current_size, compressed(bool), original_size]
    files = {}
    out = []

    def fits(owner, delta):
        cap = capacity[owner]
        if cap is None:
            return True
        return usage[owner] + delta <= cap

    for op in operations:
        kind = op[0]
        if kind == "ADD_USER":
            uid, cap_s = op[1], op[2]
            if uid == "" or uid == "admin" or uid in capacity:
                out.append("false")
            else:
                capacity[uid] = int(cap_s)
                usage[uid] = 0
                out.append("true")
        elif kind == "ADD_FILE":
            uid, path, size_s = op[1], op[2], op[3]
            size = int(size_s)
            if (uid not in capacity or path in files or size <= 0
                    or path.endswith(SUFFIX) or not fits(uid, size)):
                out.append("false")
            else:
                files[path] = [uid, size, False, size]
                usage[uid] += size
                out.append("true")
        elif kind == "COPY_FILE":
            src, dst = op[1], op[2]
            rec = files.get(src)
            if rec is None or dst in files or dst == src:
                out.append("false")
            elif dst.endswith(SUFFIX) != rec[2]:
                out.append("false")
            elif not fits(rec[0], rec[1]):
                out.append("false")
            else:
                files[dst] = [rec[0], rec[1], rec[2], rec[3]]
                usage[rec[0]] += rec[1]
                out.append("true")
        elif kind == "FIND_FILES":
            prefix, suffix = op[1], op[2]
            matches = [(rec[1], path) for path, rec in files.items()
                       if path.startswith(prefix) and path.endswith(suffix)]
            matches.sort(key=lambda t: (-t[0], t[1]))
            out.append(", ".join("%s(%d)" % (p, s) for s, p in matches))
        elif kind == "COMPRESS_FILE":
            uid, path = op[1], op[2]
            rec = files.get(path)
            new_path = path + SUFFIX
            if rec is None or rec[0] != uid or rec[2] or new_path in files:
                out.append("false")
            else:
                old = rec[1]
                new_size = (old + 1) // 2
                del files[path]
                files[new_path] = [uid, new_size, True, old]
                usage[uid] += new_size - old
                out.append("true")
        elif kind == "DECOMPRESS_FILE":
            uid, path = op[1], op[2]
            rec = files.get(path)
            if rec is None or rec[0] != uid or not rec[2] or not path.endswith(SUFFIX):
                out.append("false")
                continue
            new_path = path[:-len(SUFFIX)]
            if new_path in files or not fits(uid, rec[3] - rec[1]):
                out.append("false")
            else:
                del files[path]
                files[new_path] = [uid, rec[3], False, rec[3]]
                usage[uid] += rec[3] - rec[1]
                out.append("true")
        else:
            out.append("false")
    return out
