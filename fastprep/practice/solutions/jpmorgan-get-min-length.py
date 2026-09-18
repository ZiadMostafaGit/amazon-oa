# Stack: a 'B' cancels whatever character sits on top of the stack.
def getMinLength(seq: str) -> int:
    stack = []
    for c in seq:
        if c == 'B' and stack:
            stack.pop()
        else:
            stack.append(c)
    return len(stack)
