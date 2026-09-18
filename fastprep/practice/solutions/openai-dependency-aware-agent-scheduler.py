# Approach: Kahn topological scheduling in unit rounds, adding each agent's sequential chain edges and taking the lowest-numbered ready tasks up to the concurrency limit.
from typing import List, Optional, Any
import heapq


def solve(agentCount: int, concurrencyLimit: int, taskAgents: List[int], prerequisites: List[List[int]]) -> List[List[int]]:
    n = len(taskAgents)
    if n == 0:
        return []
    if concurrencyLimit <= 0:
        return []

    successors = [[] for _ in range(n)]
    indegree = [0] * n
    seen_edges = set()

    def add_edge(before: int, after: int) -> None:
        if before == after or (before, after) in seen_edges:
            return
        seen_edges.add((before, after))
        successors[before].append(after)
        indegree[after] += 1

    for before, after in prerequisites:
        add_edge(before, after)

    last_of_agent = {}
    for task in range(n):
        agent = taskAgents[task]
        if agent in last_of_agent:
            add_edge(last_of_agent[agent], task)
        last_of_agent[agent] = task

    ready = [t for t in range(n) if indegree[t] == 0]
    heapq.heapify(ready)

    rounds = []
    done = 0
    while ready:
        batch = []
        while ready and len(batch) < concurrencyLimit:
            batch.append(heapq.heappop(ready))
        rounds.append(batch)
        done += len(batch)
        for task in batch:
            for nxt in successors[task]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    heapq.heappush(ready, nxt)

    if done != n:
        return []
    return rounds
