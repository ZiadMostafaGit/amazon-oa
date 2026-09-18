# Build an ordered forest from the CSV rows, then emit an iterative preorder walk with branch markers.
from typing import List, Optional, Any


def renderTaskTree(rows: List[str]) -> List[str]:
    children = {}
    names = {}
    roots = []
    for row in rows:
        parts = row.split(",")
        kind = parts[1]
        if kind == "task":
            tid = parts[2]
            name = parts[3]
            roots.append(tid)
        else:
            pid = parts[2]
            tid = parts[3]
            name = parts[4]
            children.setdefault(pid, []).append(tid)
        names[tid] = name
        children.setdefault(tid, [])

    out = []
    # stack entries: (task id, depth, is_last_child) ; depth 0 == root
    stack = []
    for tid in reversed(roots):
        stack.append((tid, 0, True))
    while stack:
        tid, depth, is_last = stack.pop()
        if depth == 0:
            out.append(tid + " " + names[tid])
        else:
            marker = "\\-" if is_last else "|-"
            out.append("  " * (depth - 1) + marker + " " + tid + " " + names[tid])
        kids = children[tid]
        for i in range(len(kids) - 1, -1, -1):
            stack.append((kids[i], depth + 1, i == len(kids) - 1))
    return out
