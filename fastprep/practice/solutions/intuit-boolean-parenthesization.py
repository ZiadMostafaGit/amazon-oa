# Interval DP: T[i][j], F[i][j] = ways operands i..j evaluate to true / false; try every operator as the last one applied.
def countTrueWays(expression: str) -> int:
    vals = expression[0::2]
    ops = expression[1::2]
    n = len(vals)
    T = [[0] * n for _ in range(n)]
    F = [[0] * n for _ in range(n)]
    for i, v in enumerate(vals):
        T[i][i] = 1 if v == "T" else 0
        F[i][i] = 1 - T[i][i]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            t = f = 0
            for k in range(i, j):              # operator ops[k] splits i..k | k+1..j
                lt, lf, rt, rf = T[i][k], F[i][k], T[k + 1][j], F[k + 1][j]
                tot = (lt + lf) * (rt + rf)
                op = ops[k]
                if op == "&":
                    w = lt * rt
                elif op == "|":
                    w = tot - lf * rf
                else:
                    w = lt * rf + lf * rt
                t += w
                f += tot - w
            T[i][j], F[i][j] = t, f
    return T[0][n - 1]
