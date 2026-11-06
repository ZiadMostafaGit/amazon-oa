from typing import List, Optional, Any
import heapq


def countDeliveryPredecessors(n: int, roads: List[List[int]], capital: int) -> List[int]:
    adj = [[] for _ in range(n + 1)]
    for a, b, w in roads:
        adj[a].append((b, w))
        adj[b].append((a, w))
    INF = float("inf")
    dist = [INF] * (n + 1)
    dist[capital] = 0
    pq = [(0, capital)]
    order = []
    done = [False] * (n + 1)
    while pq:
        d, u = heapq.heappop(pq)
        if done[u]:
            continue
        done[u] = True
        order.append(u)
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    # reach[v] = bitmask of cities on some shortest route capital -> v (including v)
    reach = [0] * (n + 1)
    for u in order:
        mask = 1 << u
        for v, w in adj[u]:
            if dist[v] + w == dist[u]:
                mask |= reach[v]
        reach[u] = mask
    ans = []
    for i in range(1, n + 1):
        m = reach[i] & ~(1 << i) & ~(1 << capital)
        ans.append(bin(m).count("1"))
    return ans
