# Prefix scan forward + reverse-mode suffix accumulation S_k = U[k] + S_{k+1} @ M_{k+1}^T, grad_k = P[k-1]^T @ S_k.
from typing import List, Optional, Any


def _matmul(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    n = len(a)
    m = len(b[0])
    k = len(b)
    out = [[0] * m for _ in range(n)]
    for i in range(n):
        ai = a[i]
        oi = out[i]
        for t in range(k):
            v = ai[t]
            if v:
                bt = b[t]
                for j in range(m):
                    oi[j] += v * bt[j]
    return out


def _transpose(a: List[List[int]]) -> List[List[int]]:
    return [list(col) for col in zip(*a)]


def _identity(d: int) -> List[List[int]]:
    return [[1 if i == j else 0 for j in range(d)] for i in range(d)]


def prefixProductAutograd(matrices: List[List[List[int]]], upstream: List[List[List[int]]]) -> List[List[int]]:
    n = len(matrices)
    d = len(matrices[0])

    # Forward: inclusive prefix products.
    prefixes: List[List[List[int]]] = []
    cur = [row[:] for row in matrices[0]]
    prefixes.append(cur)
    for i in range(1, n):
        cur = _matmul(cur, matrices[i])
        prefixes.append(cur)

    # Backward: suffix accumulators.
    grads: List[List[List[int]]] = [None] * n  # type: ignore[list-item]
    s = [row[:] for row in upstream[n - 1]]
    left = prefixes[n - 2] if n >= 2 else _identity(d)
    grads[n - 1] = _matmul(_transpose(left), s)
    for k in range(n - 2, -1, -1):
        s = _matmul(s, _transpose(matrices[k + 1]))
        for r in range(d):
            ur = upstream[k][r]
            sr = s[r]
            for c in range(d):
                sr[c] += ur[c]
        left = prefixes[k - 1] if k >= 1 else _identity(d)
        grads[k] = _matmul(_transpose(left), s)

    result: List[List[int]] = []
    for mat in prefixes:
        flat = []
        for row in mat:
            flat.extend(row)
        result.append(flat)
    for mat in grads:
        flat = []
        for row in mat:
            flat.extend(row)
        result.append(flat)
    return result
