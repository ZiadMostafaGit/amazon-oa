# Monotonic increasing stack: drop a digit whenever it is larger than the next one.
def removeKdigits(num: str, k: int) -> str:
    stack = []
    remaining = k
    for ch in num:
        while remaining and stack and stack[-1] > ch:
            stack.pop()
            remaining -= 1
        stack.append(ch)
    if remaining:
        del stack[len(stack) - remaining:]
    result = "".join(stack).lstrip("0")
    return result if result else "0"
