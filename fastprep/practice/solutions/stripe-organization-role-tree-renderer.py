from typing import List


def renderOrganization(relations: List[str]) -> List[str]:
    children = {}
    root = None
    for rel in relations:
        role, parent = rel.split(",", 1)
        role, parent = role.strip(), parent.strip()
        children.setdefault(role, [])
        if parent == "":
            root = role
        else:
            children.setdefault(parent, []).append(role)
    out = []
    stack = [(root, 0)]
    while stack:
        role, d = stack.pop()
        out.append("--" * d + role)
        for c in sorted(children[role], reverse=True):  # reversed so smallest pops first
            stack.append((c, d + 1))
    return out
