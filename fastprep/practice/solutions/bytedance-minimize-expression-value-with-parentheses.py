# Brute force over every valid (open paren, close paren) placement, O(n^2) products.


def minimizeExpressionValueWithParentheses(expr: str) -> int:
    p = expr.index('+')
    left = expr[:p]
    right = expr[p + 1:]
    best = None
    for i in range(len(left)):
        outer_left = int(left[:i]) if i > 0 else 1
        inner_left = int(left[i:])
        for j in range(1, len(right) + 1):
            inner_right = int(right[:j])
            outer_right = int(right[j:]) if j < len(right) else 1
            val = outer_left * (inner_left + inner_right) * outer_right
            if best is None or val < best:
                best = val
    return best
