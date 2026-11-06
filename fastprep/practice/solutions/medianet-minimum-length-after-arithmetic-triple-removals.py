# rem[i][j]: can a[i..j] be removed completely? a[i] leaves in some triple (i, p, q). Either q == j (the
# insides i+1..p-1 and p+1..j-1 vanish first) or the block splits at q. Then a 1-D DP keeps the rest.
from typing import List


def minFinalLength(a: List[int]) -> int:
    n = len(a)

    def ok(i, j):                       # empty segments are removable
        return i > j or rem[i][j]

    rem = [[False] * n for _ in range(n)]
    for length in range(3, n + 1, 3):
        for i in range(n - length + 1):
            j = i + length - 1
            good = False
            s = a[i] + a[j]
            for p in range(i + 1, j, 3):     # i+1..p-1 removable needs (p-i-1) % 3 == 0
                if 2 * a[p] == s and ok(i + 1, p - 1) and ok(p + 1, j - 1):
                    good = True
                    break
            if not good:
                for k in range(i + 2, j - 2, 3):
                    if rem[i][k] and rem[k + 1][j]:
                        good = True
                        break
            rem[i][j] = good
    best = [0] * (n + 1)                # best[j] = min length of a prefix of length j
    for j in range(1, n + 1):
        b = best[j - 1] + 1
        for i in range(j - 3, -1, -3):
            if rem[i][j - 1] and best[i] < b:
                b = best[i]
        best[j] = b
    return best[n]
