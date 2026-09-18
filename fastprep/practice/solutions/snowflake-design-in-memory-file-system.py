# Trie of directory dicts with files stored as string values; replay operations in order.
from typing import List, Optional, Any


def executeFileSystem(operations: List[List[str]]) -> List[List[str]]:
    root = {}  # name -> dict (directory) or list[str] (file content chunks)

    def split(path: str) -> List[str]:
        return [p for p in path.split("/") if p]

    def walk(parts: List[str], create: bool):
        node = root
        for p in parts:
            if p not in node:
                if not create:
                    return None
                node[p] = {}
            node = node[p]
        return node

    out = []
    for op in operations:
        kind = op[0]
        if kind == "mkdir":
            walk(split(op[1]), True)
        elif kind == "addContentToFile":
            parts = split(op[1])
            parent = walk(parts[:-1], True)
            name = parts[-1]
            if name in parent and isinstance(parent[name], list):
                parent[name].append(op[2])
            else:
                parent[name] = [op[2]]
        elif kind == "readContentFromFile":
            parts = split(op[1])
            parent = walk(parts[:-1], False)
            out.append(["".join(parent[parts[-1]])])
        elif kind == "ls":
            parts = split(op[1])
            if not parts:
                out.append(sorted(root.keys()))
                continue
            parent = walk(parts[:-1], False)
            name = parts[-1]
            entry = parent[name]
            if isinstance(entry, list):
                out.append([name])
            else:
                out.append(sorted(entry.keys()))
    return out
