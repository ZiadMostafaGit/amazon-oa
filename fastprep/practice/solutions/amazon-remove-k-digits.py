# Monotonic increasing stack: pop larger leading digits while removals remain.
def removeKdigits(num: str, k: int) -> str:
    stack = []
    for ch in num:
        while k > 0 and stack and stack[-1] > ch:
            stack.pop()
            k -= 1
        stack.append(ch)
    if k > 0:
        stack = stack[:len(stack) - k]
    result = "".join(stack).lstrip("0")
    return result if result else "0"
