# Family tree with children lists plus a dead set; each ORDER runs an iterative pre-order DFS.
from typing import List, Optional, Any


def inheritanceOrders(operations: List[List[str]]) -> List[List[str]]:
    children = {}
    dead = set()
    founder = None
    res = []
    for op in operations:
        kind = op[0]
        if kind == "BIRTH":
            parent, child = op[1], op[2]
            if founder is None:
                founder = parent
                children[parent] = []
            children.setdefault(parent, []).append(child)
            children[child] = []
        elif kind == "DEATH":
            dead.add(op[1])
        else:
            order = []
            if founder is not None:
                stack = [founder]
                while stack:
                    name = stack.pop()
                    if name not in dead:
                        order.append(name)
                    kids = children.get(name, ())
                    for i in range(len(kids) - 1, -1, -1):
                        stack.append(kids[i])
            res.append(order)
    return res
