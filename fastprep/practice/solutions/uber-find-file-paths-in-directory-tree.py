# Build a trie of path components, then walk it with an explicit stack collecting matching leaves.
from typing import List, Optional, Any


def findFilePaths(directoryPaths: List[str], filePaths: List[str], targetName: str) -> List[str]:
    root = {"name": "", "children": {}, "is_file": False}

    def insert(path: str, is_file: bool) -> None:
        parts = [p for p in path.split("/") if p != ""]
        node = root
        for idx, part in enumerate(parts):
            child = node["children"].get(part)
            if child is None:
                child = {"name": part, "children": {}, "is_file": False}
                node["children"][part] = child
            node = child
        if is_file:
            node["is_file"] = True

    for d in directoryPaths:
        insert(d, False)
    for f in filePaths:
        insert(f, True)

    res = []
    stack = [(root, "")]
    while stack:
        node, prefix = stack.pop()
        if node is not root:
            if node["is_file"] and node["name"] == targetName:
                res.append(prefix)
        for child in node["children"].values():
            stack.append((child, prefix + "/" + child["name"]))
    res.sort()
    return res
