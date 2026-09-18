# Three passes: hash-set dedupe, forest build over non-completed survivors, then iterative preorder with sorted sibling lists.
from typing import List, Dict


def orderHierarchicalTasks(taskIds: List[str], descriptions: List[str], dueDates: List[int],
                           priorities: List[int], completed: List[bool],
                           parentIds: List[str]) -> List[str]:
    n = len(taskIds)

    # Phase 1: keep the first occurrence of each (description, due date) pair.
    seen = set()
    kept: List[int] = []
    for i in range(n):
        key = (descriptions[i], dueDates[i])
        if key in seen:
            continue
        seen.add(key)
        kept.append(i)

    # Phase 2: among retained tasks, candidates are the uncompleted ones.
    rank: Dict[str, int] = {}
    candidate: Dict[str, int] = {}
    for pos, i in enumerate(kept):
        rank[taskIds[i]] = pos
        if not completed[i]:
            candidate[taskIds[i]] = i

    children: Dict[str, List[str]] = {}
    roots: List[str] = []
    for tid, i in candidate.items():
        par = parentIds[i]
        if par == "":
            roots.append(tid)
        elif par in candidate:
            children.setdefault(par, []).append(tid)
        # otherwise the parent did not survive, so this subtree is dropped

    def sort_key(tid: str):
        i = candidate[tid]
        return (-priorities[i], dueDates[i], rank[tid])

    roots.sort(key=sort_key)
    for lst in children.values():
        lst.sort(key=sort_key)

    # Phase 3: iterative preorder over the surviving forest.
    out: List[str] = []
    stack = roots[::-1]
    while stack:
        tid = stack.pop()
        out.append(tid)
        kids = children.get(tid)
        if kids:
            stack.extend(reversed(kids))
    return out
