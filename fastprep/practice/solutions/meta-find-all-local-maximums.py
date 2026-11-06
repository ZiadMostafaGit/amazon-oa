from typing import List, Optional, Any


def findAllLocalMaximums(matrix: List[List[int]]) -> List[List[int]]:
    n = len(matrix)
    m = len(matrix[0]) if n else 0
    out = []
    for i in range(n):
        for j in range(m):
            v = matrix[i][j]
            if v == 0:
                continue
            ok = True
            for r in range(max(0, i - v), min(n, i + v + 1)):
                if not ok:
                    break
                for c in range(max(0, j - v), min(m, j + v + 1)):
                    if r == i and c == j:
                        continue
                    if abs(r - i) == v and abs(c - j) == v:
                        continue  # corner
                    if matrix[r][c] >= v:
                        ok = False
                        break
            if ok:
                out.append([i, j])
    return out
