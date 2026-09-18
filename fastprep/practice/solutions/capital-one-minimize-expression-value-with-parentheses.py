# Brute force over every valid left/right parenthesis position (expr length <= 10).
def minimizeExpressionValueWithParentheses(expr: str) -> int:
    n = len(expr)
    p = expr.index('+')
    best = None
    # left paren goes before index i, so addend a = expr[i:p] must be non-empty
    for i in range(0, p):
        left = int(expr[:i]) if i > 0 else 1
        a = int(expr[i:p])
        # right paren goes after index k, so addend b = expr[p+1:k+1] must be non-empty
        for k in range(p + 1, n):
            b = int(expr[p + 1:k + 1])
            right = int(expr[k + 1:]) if k + 1 < n else 1
            val = left * (a + b) * right
            if best is None or val < best:
                best = val
    return best
