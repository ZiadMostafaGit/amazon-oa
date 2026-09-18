# Approach: iterative DFS post-order topological sort from the target with cycle detection.
from typing import List, Optional, Any


def packageInstallOrder(dependencies: List[List[str]], target: str) -> List[str]:
    graph = {}
    for pair in dependencies:
        if len(pair) < 2:
            continue
        pkg, dep = pair[0], pair[1]
        graph.setdefault(pkg, []).append(dep)
        graph.setdefault(dep, [])
    if target not in graph:
        return [target]

    order = []
    state = {}  # 0 = visiting, 1 = done
    # stack entries: (node, index of next dependency to explore)
    stack = [[target, 0]]
    state[target] = 0
    while stack:
        frame = stack[-1]
        node, idx = frame[0], frame[1]
        deps = graph.get(node, [])
        if idx < len(deps):
            frame[1] += 1
            nxt = deps[idx]
            st = state.get(nxt)
            if st == 0:
                return []  # cycle
            if st is None:
                state[nxt] = 0
                stack.append([nxt, 0])
        else:
            state[node] = 1
            order.append(node)
            stack.pop()
    return order
