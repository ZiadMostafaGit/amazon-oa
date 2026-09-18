# Tokenize into parens/atoms, build serialized JSON with an explicit stack of child lists.


def parseLispExpression(expression: str) -> str:
    tokens = []
    i = 0
    n = len(expression)
    ws = " \t\n\r"
    while i < n:
        c = expression[i]
        if c in ws:
            i += 1
        elif c == '(' or c == ')':
            tokens.append(c)
            i += 1
        else:
            j = i
            while j < n and expression[j] not in ws and expression[j] != '(' and expression[j] != ')':
                j += 1
            tokens.append(expression[i:j])
            i = j

    stack = []  # list of lists of serialized children
    result = None
    for tok in tokens:
        if tok == '(':
            stack.append([])
        elif tok == ')':
            children = stack.pop()
            s = '[' + ','.join(children) + ']'
            if stack:
                stack[-1].append(s)
            else:
                result = s
        else:
            s = '"' + tok + '"'
            if stack:
                stack[-1].append(s)
            else:
                result = s
    return result if result is not None else ""
