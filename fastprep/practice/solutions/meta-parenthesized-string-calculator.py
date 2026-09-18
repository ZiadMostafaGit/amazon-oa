# Single-pass stack scan: keep a running sign and push (result, sign) on '('.


def calculate(expression: str) -> int:
    result = 0
    sign = 1
    num = 0
    stack = []
    for ch in expression:
        if ch.isdigit():
            num = num * 10 + (ord(ch) - 48)
        elif ch == '+':
            result += sign * num
            num = 0
            sign = 1
        elif ch == '-':
            result += sign * num
            num = 0
            sign = -1
        elif ch == '(':
            stack.append((result, sign))
            result = 0
            sign = 1
        elif ch == ')':
            result += sign * num
            num = 0
            prev_result, prev_sign = stack.pop()
            result = prev_result + prev_sign * result
            sign = 1
        # spaces and any other characters are ignored
    return result + sign * num
