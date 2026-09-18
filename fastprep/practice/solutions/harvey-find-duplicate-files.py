# Iterative BFS over a snapshot with symlink resolution, then group files by exact content.
from typing import List, Optional, Any
from collections import deque


def findDuplicateFiles(root: str, entries: List[List[str]]) -> List[List[str]]:
    info = {}
    for path, kind, target, content, readable in entries:
        info[path] = (kind, target, content, readable == "1")

    children = {}
    for path in info:
        if path == "/":
            continue
        idx = path.rfind("/")
        parent = path[:idx] if idx > 0 else "/"
        children.setdefault(parent, []).append(path)
    for kids in children.values():
        kids.sort()

    def resolve(path):
        # follow a symbolic-link chain to a real entry, or None if broken/cyclic/unreadable
        seen = set()
        cur = path
        while True:
            if cur in seen or cur not in info:
                return None
            entry = info[cur]
            if not entry[3]:
                return None
            if entry[0] != "L":
                return cur
            seen.add(cur)
            cur = entry[1]

    start = resolve(root)
    if start is None or info[start][0] != "D":
        return []

    visited_dirs = {start}
    # real file path -> (smallest access path, content)
    files = {}
    queue = deque([start])
    while queue:
        directory = queue.popleft()
        for child in children.get(directory, []):
            entry = info[child]
            if not entry[3]:
                continue
            real = resolve(child)
            if real is None:
                continue
            kind = info[real][0]
            if kind == "D":
                if real not in visited_dirs:
                    visited_dirs.add(real)
                    queue.append(real)
            elif kind == "F":
                content = info[real][2]
                best = files.get(real)
                if best is None or child < best[0]:
                    files[real] = (child, content)

    by_content = {}
    for access, content in files.values():
        by_content.setdefault(content, []).append(access)

    groups = [sorted(paths) for paths in by_content.values() if len(paths) >= 2]
    groups.sort(key=lambda g: g[0])
    return groups
