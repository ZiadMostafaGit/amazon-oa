from typing import List, Optional, Any


def createWorkflowStages(precursorSteps: List[List[str]]) -> List[List[str]]:
    adj = {}
    indeg = {}
    for before, after in precursorSteps:
        adj.setdefault(before, set())
        adj.setdefault(after, set())
        indeg.setdefault(before, 0)
        indeg.setdefault(after, 0)
        if after not in adj[before]:
            adj[before].add(after)
            indeg[after] += 1
    stages = []
    layer = sorted(s for s in indeg if indeg[s] == 0)
    while layer:
        stages.append(layer)
        nxt = []
        for u in layer:
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    nxt.append(v)
        layer = sorted(nxt)
    return stages
