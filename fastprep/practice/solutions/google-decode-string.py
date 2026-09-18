# Stack-based decoding: push (prefix, count) on '[', pop and repeat on ']'.
def decodeString(s: str) -> str:
    stack = []
    cur = []
    num = 0
    for ch in s:
        if ch.isdigit():
            num = num * 10 + (ord(ch) - 48)
        elif ch == '[':
            stack.append((cur, num))
            cur = []
            num = 0
        elif ch == ']':
            prev, k = stack.pop()
            prev.append(''.join(cur) * k)
            cur = prev
        else:
            cur.append(ch)
    return ''.join(cur)
