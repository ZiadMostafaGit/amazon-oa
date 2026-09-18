# Dict of directory path -> set of file names, with a per-base counter for collision suffixes.
from typing import List, Optional, Any


def _split_ext(name: str):
    idx = name.rfind('.')
    if 0 < idx < len(name) - 1:
        return name[:idx], name[idx:]
    return name, ""


def runVault(operations: List[str], paths: List[str]) -> List[List[str]]:
    files = {}
    next_try = {}
    out = []
    for op, path in zip(operations, paths):
        if op == "add_file":
            cut = path.rfind('/')
            directory = path[:cut]
            if directory == "":
                directory = "/"
            name = path[cut + 1:]
            bucket = files.setdefault(directory, set())
            if name not in bucket:
                bucket.add(name)
            else:
                stem, ext = _split_ext(name)
                key = (directory, name)
                x = next_try.get(key, 1)
                while True:
                    candidate = stem + "(" + str(x) + ")" + ext
                    x += 1
                    if candidate not in bucket:
                        break
                next_try[key] = x
                bucket.add(candidate)
        else:
            directory = path
            if len(directory) > 1 and directory.endswith('/'):
                directory = directory.rstrip('/')
                if directory == "":
                    directory = "/"
            out.append(sorted(files.get(directory, ())))
    return out
