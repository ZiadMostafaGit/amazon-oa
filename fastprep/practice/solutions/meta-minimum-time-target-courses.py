# Iterative DFS with memoization over the reverse prerequisite DAG (longest path to each target).
from typing import List, Optional, Any


def minimumTimeForTargets(durations: List[int], prerequisites: List[List[int]], targets: List[int]) -> int:
    n = len(durations)
    preds = [[] for _ in range(n)]
    for pair in prerequisites:
        course, prereq = pair[0], pair[1]
        preds[course].append(prereq)

    finish = [-1] * n
    answer = 0
    for t in targets:
        if finish[t] >= 0:
            answer = max(answer, finish[t])
            continue
        stack = [(t, 0)]
        while stack:
            node, idx = stack.pop()
            if finish[node] >= 0:
                continue
            plist = preds[node]
            if idx < len(plist):
                stack.append((node, idx + 1))
                nxt = plist[idx]
                if finish[nxt] < 0:
                    stack.append((nxt, 0))
            else:
                best = 0
                for p in plist:
                    if finish[p] > best:
                        best = finish[p]
                finish[node] = best + durations[node]
        answer = max(answer, finish[t])
    return answer
