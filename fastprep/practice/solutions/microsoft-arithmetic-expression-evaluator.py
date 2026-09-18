# Iterative shunting-yard: operator/value stacks with unary sign handling and truncate-toward-zero division.
PREC = {'u': 3, '*': 2, '/': 2, '+': 1, '-': 1}


def _apply(values, op):
    if op == 'u':
        values.append(-values.pop())
        return
    b = values.pop()
    a = values.pop()
    if op == '+':
        values.append(a + b)
    elif op == '-':
        values.append(a - b)
    elif op == '*':
        values.append(a * b)
    else:
        q = abs(a) // abs(b)
        if (a < 0) != (b < 0):
            q = -q
        values.append(q)


def evaluateExpression(expression: str) -> int:
    values = []
    ops = []
    expect_operand = True
    i = 0
    n = len(expression)
    while i < n:
        c = expression[i]
        if c == ' ':
            i += 1
            continue
        if c.isdigit():
            j = i
            while j < n and expression[j].isdigit():
                j += 1
            values.append(int(expression[i:j]))
            i = j
            expect_operand = False
            continue
        if c == '(':
            ops.append('(')
            expect_operand = True
        elif c == ')':
            while ops and ops[-1] != '(':
                _apply(values, ops.pop())
            if ops:
                ops.pop()
            expect_operand = False
        else:
            if expect_operand:
                # unary sign: '+' is a no-op, '-' negates
                if c == '-':
                    ops.append('u')
                # expect_operand stays True
            else:
                p = PREC[c]
                while ops and ops[-1] != '(' and PREC[ops[-1]] >= p:
                    _apply(values, ops.pop())
                ops.append(c)
                expect_operand = True
        i += 1
    while ops:
        op = ops.pop()
        if op != '(':
            _apply(values, op)
    return values[-1] if values else 0
