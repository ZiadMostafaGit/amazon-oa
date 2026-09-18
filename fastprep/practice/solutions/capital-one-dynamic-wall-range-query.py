# Fenwick (BIT) over wall indicators; range query = prefix-sum difference > 0.
from typing import List, Optional, Any


def solveOneDynamicWallRangeQuery(input: str) -> List[str]:
    lines = input.split("\n")
    idx = 0

    def next_line() -> str:
        nonlocal idx
        while idx < len(lines):
            s = lines[idx].strip()
            idx += 1
            if s:
                return s
        return ""

    n_tok = next_line()
    if not n_tok:
        return []
    n = int(n_tok)
    q_tok = next_line()
    q = int(q_tok) if q_tok else 0

    tree = [0] * (n + 1)
    built = [False] * (n + 1)

    def update(i: int) -> None:
        i += 1
        while i <= n:
            tree[i] += 1
            i += i & (-i)

    def prefix(i: int) -> int:
        # sum of indices 0..i
        i += 1
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & (-i)
        return s

    out: List[str] = []
    for _ in range(q):
        line = next_line()
        if not line:
            break
        parts = line.split()
        op = parts[0]
        if op == "build":
            i = int(parts[1])
            if 0 <= i < n and not built[i]:
                built[i] = True
                update(i)
        elif op == "query":
            l = int(parts[1])
            r = int(parts[2])
            if l > r or l >= n:
                out.append("0")
                continue
            r = min(r, n - 1)
            l = max(l, 0)
            total = prefix(r) - (prefix(l - 1) if l > 0 else 0)
            out.append("1" if total > 0 else "0")
    return out
