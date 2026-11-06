from typing import List, Optional, Any


def searchMysteriousGrid(phrases: List[str], grid: List[List[str]]) -> int:
    n = len(grid)
    m = len(grid[0]) if n else 0
    total = 0
    for w in phrases:
        L = len(w)
        if L == 0:
            continue
        if L == 1:
            total += sum(1 for r in range(n) for c in range(m) if grid[r][c] == w)
            continue
        for i in range(n):
            for j in range(m):
                if grid[i][j] != w[0]:
                    continue
                for di, dj in ((0, 1), (1, 0)):
                    # f = how many letters match going forward from (i, j)
                    f = 0
                    r, c = i, j
                    while f < L and 0 <= r < n and 0 <= c < m and grid[r][c] == w[f]:
                        f += 1
                        r += di
                        c += dj
                    if f == L:
                        total += 1  # straight path, no turn
                    # turn after letter t (t >= 1): letters t+1.. walk back
                    for t in range(1, min(f, L - 1)):
                        r, c = i + di * t, j + dj * t
                        ok = True
                        for k in range(t + 1, L):
                            r -= di
                            c -= dj
                            if not (0 <= r < n and 0 <= c < m) or grid[r][c] != w[k]:
                                ok = False
                                break
                        if ok:
                            total += 1
    return total
