# Tree DP over three label classes (the prime 2, primes p with p+2 prime, the rest).
from typing import List, Optional, Any


def countPrimeLabelings(n: int, edgeFrom: List[int], edgeTo: List[int]) -> int:
    MOD = 10 ** 9 + 7

    def is_prime(x: int) -> bool:
        if x < 2:
            return False
        i = 2
        while i * i <= x:
            if x % i == 0:
                return False
            i += 1
        return True

    primes = [p for p in range(2, 101) if is_prime(p)]
    # class 0: the label 2 (the only even prime)
    # class 1: odd primes q with q + 2 prime  -> forbidden next to a 2
    # class 2: odd primes q with q + 2 composite -> unrestricted
    cntB = sum(1 for q in primes if q != 2 and is_prime(q + 2))
    cntC = len(primes) - 1 - cntB

    if n == 1:
        return len(primes) % MOD

    adj_head = [-1] * (n + 1)
    nxt = [-1] * (2 * (n - 1))
    dest = [0] * (2 * (n - 1))
    idx = 0
    for u, v in zip(edgeFrom, edgeTo):
        dest[idx] = v
        nxt[idx] = adj_head[u]
        adj_head[u] = idx
        idx += 1
        dest[idx] = u
        nxt[idx] = adj_head[v]
        adj_head[v] = idx
        idx += 1

    # iterative DFS producing a parent array and a reverse topological order
    parent = [0] * (n + 1)
    order = []
    visited = [False] * (n + 1)
    stack = [1]
    visited[1] = True
    while stack:
        u = stack.pop()
        order.append(u)
        e = adj_head[u]
        while e != -1:
            w = dest[e]
            if not visited[w]:
                visited[w] = True
                parent[w] = u
                stack.append(w)
            e = nxt[e]

    d0 = [1] * (n + 1)
    d1 = [cntB % MOD] * (n + 1)
    d2 = [cntC % MOD] * (n + 1)

    for u in reversed(order):
        p = parent[u]
        if p:
            # a "2" parent forbids class-1 children; a class-1 parent forbids "2" children
            d0[p] = d0[p] * ((d0[u] + d2[u]) % MOD) % MOD
            d1[p] = d1[p] * ((d1[u] + d2[u]) % MOD) % MOD
            d2[p] = d2[p] * ((d0[u] + d1[u] + d2[u]) % MOD) % MOD

    return (d0[1] + d1[1] + d2[1]) % MOD
