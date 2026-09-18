# Single left-to-right scan dropping unmatched ')', then drop leftover '(' positions.
def makeParenthesesBalanced(s: str) -> str:
    keep = [True] * len(s)
    stack = []
    for i, ch in enumerate(s):
        if ch == '(':
            stack.append(i)
        elif ch == ')':
            if stack:
                stack.pop()
            else:
                keep[i] = False
    for i in stack:
        keep[i] = False
    return ''.join(ch for i, ch in enumerate(s) if keep[i])
