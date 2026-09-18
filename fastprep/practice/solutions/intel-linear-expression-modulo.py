# Shunting-yard parse into a linear polynomial (a*x+b) mod m, then solve a*x = c (mod m) by extended gcd.


def _egcd(a: int, b: int):
    old_r, r = a, b
    old_s, s = 1, 0
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
    return old_r, old_s


def smallestNonnegativeX(expression: str, p: int, m: int) -> int:
    # tokenize
    tokens = []
    i = 0
    n = len(expression)
    while i < n:
        ch = expression[i]
        if ch.isspace():
            i += 1
            continue
        if ch.isdigit():
            j = i
            while j < n and expression[j].isdigit():
                j += 1
            tokens.append(("num", int(expression[i:j]) % m))
            i = j
            continue
        if ch == 'x':
            tokens.append(("var", 0))
            i += 1
            continue
        tokens.append((ch, 0))
        i += 1

    prec = {'+': 1, '-': 1, '*': 2}
    vals = []
    ops = []

    def apply():
        op = ops.pop()
        a2, b2 = vals.pop()
        a1, b1 = vals.pop()
        if op == '+':
            vals.append(((a1 + a2) % m, (b1 + b2) % m))
        elif op == '-':
            vals.append(((a1 - a2) % m, (b1 - b2) % m))
        else:
            vals.append(((a1 * b2 + a2 * b1) % m, (b1 * b2) % m))

    for kind, val in tokens:
        if kind == "num":
            vals.append((0, val))
        elif kind == "var":
            vals.append((1 % m, 0))
        elif kind == '(':
            ops.append('(')
        elif kind == ')':
            while ops and ops[-1] != '(':
                apply()
            ops.pop()
        else:
            while ops and ops[-1] != '(' and prec[ops[-1]] >= prec[kind]:
                apply()
            ops.append(kind)
    while ops:
        apply()

    a, b = vals[-1]
    a %= m
    c = (p - b) % m
    if a == 0:
        return 0
    g, inv = _egcd(a, m)
    if c % g:
        return 0
    mm = m // g
    return ((c // g) * (inv % mm)) % mm
