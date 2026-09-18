# BFS over the directed link graph built from the parsed stdin payload.
from typing import List, Optional, Any
from collections import deque, defaultdict


def solveMinimumWikiClicks(input: str) -> List[str]:
    lines = [ln.strip() for ln in input.replace("\r\n", "\n").split("\n")]
    lines = [ln for ln in lines if ln != ""]
    if not lines:
        return ["-1"]

    try:
        m = int(lines[0].split()[0])
    except (ValueError, IndexError):
        return ["-1"]

    body = lines[1:]
    if m > len(body):
        m = len(body)

    edge_lines = body[:m]
    if len(body) > m:
        query_line = body[m]
    elif body:
        # Malformed payload: the final edge line doubles as the query line.
        query_line = body[-1]
    else:
        return ["-1"]

    graph = defaultdict(list)
    for ln in edge_lines:
        parts = ln.split()
        if len(parts) >= 2:
            graph[parts[0]].append(parts[1])

    parts = query_line.split()
    if len(parts) < 2:
        return ["-1"]
    start, target = parts[0], parts[1]

    if start == target:
        return ["0"]

    dist = {start: 0}
    q = deque([start])
    while q:
        node = q.popleft()
        d = dist[node]
        for nxt in graph.get(node, ()):
            if nxt not in dist:
                dist[nxt] = d + 1
                if nxt == target:
                    return [str(d + 1)]
                q.append(nxt)

    return ["-1"]
