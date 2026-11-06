# Stack of (text before the group, repeat count): '[' saves the context, ']' restores it.
def decodeString(s: str) -> str:
    stack = []
    cur = []
    num = 0
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch == '[':
            stack.append((cur, num))
            cur, num = [], 0
        elif ch == ']':
            prev, k = stack.pop()
            prev.append(''.join(cur) * k)
            cur = prev
        else:
            cur.append(ch)
    return ''.join(cur)
