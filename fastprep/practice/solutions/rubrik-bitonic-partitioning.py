from typing import List, Optional, Any


def bitonicPartitioning(arr: List[int]) -> str:
    n = len(arr)
    pre = [0]
    for x in arr:
        pre.append(pre[-1] + x)

    def less(a, b, c, d):
        # mean(arr[a..b]) < mean(arr[c..d]), compared exactly with integers
        return (pre[b + 1] - pre[a]) * (d - c + 1) < (pre[d + 1] - pre[c]) * (b - a + 1)

    # inc[i][j]: partitions of arr[0..j], last segment [i..j], means strictly increasing
    inc = [[0] * n for _ in range(n)]
    for j in range(n):
        inc[0][j] = 1
    for i in range(1, n):
        for j in range(i, n):
            s = 0
            for h in range(i):
                if inc[h][i - 1] and less(h, i - 1, i, j):
                    s += inc[h][i - 1]
            inc[i][j] = s
    # dec[i][j]: partitions of arr[i..n-1], first segment [i..j], means strictly decreasing
    dec = [[0] * n for _ in range(n)]
    for i in range(n):
        dec[i][n - 1] = 1
    for j in range(n - 2, -1, -1):
        for i in range(j, -1, -1):
            s = 0
            for l in range(j + 1, n):
                if dec[j + 1][l] and less(j + 1, l, i, j):
                    s += dec[j + 1][l]
            dec[i][j] = s
    total = 0
    for i in range(1, n):
        for j in range(i, n - 1):
            left = 0
            for h in range(i):
                if inc[h][i - 1] and less(h, i - 1, i, j):
                    left += inc[h][i - 1]
            if not left:
                continue
            right = 0
            for l in range(j + 1, n):
                if dec[j + 1][l] and less(j + 1, l, i, j):
                    right += dec[j + 1][l]
            total += left * right
    return str(total)
