# Recursive-descent / stack evaluation of an infix expression with parentheses and unary signs.
def solve(s: str) -> int:
    pos = 0
    n = len(s)

    def skip():
        nonlocal pos
        while pos < n and s[pos] == ' ':
            pos += 1

    def parse_atom() -> int:
        nonlocal pos
        skip()
        if pos < n and s[pos] == '(':
            pos += 1
            v = parse_expr()
            skip()
            if pos < n and s[pos] == ')':
                pos += 1
            return v
        if pos < n and s[pos] == '+':
            pos += 1
            return parse_atom()
        if pos < n and s[pos] == '-':
            pos += 1
            return -parse_atom()
        start = pos
        while pos < n and s[pos].isdigit():
            pos += 1
        return int(s[start:pos]) if pos > start else 0

    def parse_term() -> int:
        nonlocal pos
        v = parse_atom()
        while True:
            skip()
            if pos < n and s[pos] in '*/':
                op = s[pos]
                pos += 1
                r = parse_atom()
                if op == '*':
                    v = v * r
                else:
                    q = abs(v) // abs(r)
                    v = q if (v < 0) == (r < 0) else -q
            else:
                return v

    def parse_expr() -> int:
        nonlocal pos
        v = parse_term()
        while True:
            skip()
            if pos < n and s[pos] in '+-':
                op = s[pos]
                pos += 1
                r = parse_term()
                v = v + r if op == '+' else v - r
            else:
                return v

    return parse_expr()
