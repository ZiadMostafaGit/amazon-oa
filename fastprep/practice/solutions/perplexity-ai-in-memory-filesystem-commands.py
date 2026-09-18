# Simulation over a directory trie: resolve each path to components, then apply the command.
from typing import List, Optional, Any


def runFileSystem(operations: List[List[str]]) -> List[str]:
    # a directory is a dict of name -> node; a file is None
    root = {}
    cwd: List[str] = []
    out: List[str] = []

    def resolve(path: str) -> List[str]:
        if path == "/":
            return []
        if path.startswith("/"):
            return path[1:].split("/")
        return cwd + path.split("/")

    def walk(parts: List[str]):
        node = root
        for p in parts:
            if not isinstance(node, dict) or p not in node:
                return False, None
            node = node[p]
        return True, node

    def parent_of(parts: List[str]):
        ok, node = walk(parts[:-1])
        if not ok or not isinstance(node, dict):
            return None
        return node

    for op in operations:
        cmd = op[0]
        path = op[1]
        parts = resolve(path)

        if cmd == "MKDIR" or cmd == "TOUCH":
            if not parts:
                out.append("false")
                continue
            par = parent_of(parts)
            if par is None or parts[-1] in par:
                out.append("false")
                continue
            par[parts[-1]] = {} if cmd == "MKDIR" else None
            out.append("true")

        elif cmd == "LS":
            ok, node = walk(parts)
            if not ok or not isinstance(node, dict):
                out.append("NULL")
            else:
                out.append(",".join(sorted(node.keys())))

        elif cmd == "RM":
            if not parts:
                out.append("false")
                continue
            par = parent_of(parts)
            if par is None or parts[-1] not in par or isinstance(par[parts[-1]], dict):
                out.append("false")
                continue
            del par[parts[-1]]
            out.append("true")

        elif cmd == "RMDIR":
            if not parts:
                out.append("false")
                continue
            ok, node = walk(parts)
            if not ok or not isinstance(node, dict) or node:
                out.append("false")
                continue
            # cannot remove the current directory or any of its ancestors
            if len(parts) <= len(cwd) and cwd[:len(parts)] == parts:
                out.append("false")
                continue
            par = parent_of(parts)
            del par[parts[-1]]
            out.append("true")

        elif cmd == "CD":
            ok, node = walk(parts)
            if not ok or not isinstance(node, dict):
                out.append("false")
            else:
                cwd = parts
                out.append("true")

        else:
            out.append("false")

    return out
