# Increasing radius + exact minimum set cover (branch and bound on bitmasks with an
# independent-witness lower bound) to test whether k diamonds of that radius cover the grid.
import sys


def minimumMaximumDistance(rows: int, columns: int, k: int) -> int:
    n = rows * columns
    cells = [(r, c) for r in range(rows) for c in range(columns)]
    dist = [[abs(cells[i][0] - cells[j][0]) + abs(cells[i][1] - cells[j][1])
             for j in range(n)] for i in range(n)]
    full = (1 << n) - 1
    if k >= n:
        return 0

    max_d = (rows - 1) + (columns - 1)
    sys.setrecursionlimit(10000)

    for d in range(0, max_d + 1):
        cover = [0] * n
        for i in range(n):
            m = 0
            for j in range(n):
                if dist[i][j] <= d:
                    m |= 1 << j
            cover[i] = m
        # centers that cover a given cell
        cands = [[i for i in range(n) if cover[i] >> j & 1] for j in range(n)]
        # order candidates by how much they cover (greedy-first helps find solutions fast)
        for j in range(n):
            cands[j].sort(key=lambda i: -bin(cover[i]).count("1"))

        fail = {}

        def lower_bound(uncovered):
            # greedy set of cells pairwise farther than 2d apart: each needs its own center
            witnesses = []
            m = uncovered
            while m:
                b = m & -m
                j = b.bit_length() - 1
                m ^= b
                ok = True
                for w in witnesses:
                    if dist[w][j] <= 2 * d:
                        ok = False
                        break
                if ok:
                    witnesses.append(j)
            return len(witnesses)

        def solve(uncovered, budget):
            if uncovered == 0:
                return True
            if budget == 0:
                return False
            prev = fail.get(uncovered)
            if prev is not None and prev >= budget:
                return False
            if lower_bound(uncovered) > budget:
                fail[uncovered] = max(prev or 0, budget)
                return False
            # pick the uncovered cell with the fewest possible centers
            best_j = -1
            best_len = None
            m = uncovered
            while m:
                b = m & -m
                j = b.bit_length() - 1
                m ^= b
                L = len(cands[j])
                if best_len is None or L < best_len:
                    best_len = L
                    best_j = j
            for c in cands[best_j]:
                if solve(uncovered & ~cover[c], budget - 1):
                    return True
            fail[uncovered] = max(prev or 0, budget)
            return False

        if solve(full, k):
            return d
    return max_d
