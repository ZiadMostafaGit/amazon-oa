# Topological order over the subgroup DAG, rolling up membership bitmasks so duplicates collapse.
from typing import List, Optional, Any


def groupOverdueRollup(employeeIds: List[str], dueDays: List[int], completionDays: List[int], groupNames: List[str], directEmployees: List[List[str]], directSubgroups: List[List[str]], checkDay: int) -> List[List[int]]:
    emp_index = {e: i for i, e in enumerate(employeeIds)}
    n_emp = len(employeeIds)

    overdue = [0] * n_emp
    for i in range(n_emp):
        if completionDays[i] == -1 or completionDays[i] > checkDay:
            d = checkDay - dueDays[i]
            overdue[i] = d if d > 0 else 0

    g_index = {g: i for i, g in enumerate(groupNames)}
    n_g = len(groupNames)
    children = [[] for _ in range(n_g)]
    for i in range(n_g):
        for sub in directSubgroups[i]:
            j = g_index.get(sub)
            if j is not None:
                children[i].append(j)

    # Iterative post-order DFS to get a topological (children-before-parent) order.
    state = [0] * n_g  # 0 unvisited, 1 in progress, 2 done
    order = []
    for s in range(n_g):
        if state[s] != 0:
            continue
        stack = [(s, 0)]
        state[s] = 1
        while stack:
            node, ptr = stack.pop()
            if ptr < len(children[node]):
                stack.append((node, ptr + 1))
                nxt = children[node][ptr]
                if state[nxt] == 0:
                    state[nxt] = 1
                    stack.append((nxt, 0))
            else:
                state[node] = 2
                order.append(node)

    masks = [0] * n_g
    for g in order:
        m = 0
        for e in directEmployees[g]:
            idx = emp_index.get(e)
            if idx is not None:
                m |= 1 << idx
        for c in children[g]:
            m |= masks[c]
        masks[g] = m

    result = []
    for g in range(n_g):
        m = masks[g]
        count = 0
        total = 0
        idx = 0
        while m:
            low = m & -m
            idx = low.bit_length() - 1
            count += 1
            total += overdue[idx]
            m ^= low
        result.append([count, total])
    return result
