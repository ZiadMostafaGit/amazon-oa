# Run-length boundary model: greedily push the rightmost run boundary to the end, handling length-1 runs.
def getMaximumOperations(s: str) -> int:
    n = len(s)
    start = -1
    for k in range(n - 1):
        if s[k] == s[k + 1]:
            start = k
            break
    if start < 0:
        return 0

    runs = []
    for ch in s[start:]:
        if runs and runs[-1][0] == ch:
            runs[-1][1] += 1
        else:
            runs.append([ch, 1])
    if len(runs) == 1:
        return 0

    tail_char, tail_len = runs[-1]
    stack = runs[:-1]
    big = [idx for idx, r in enumerate(stack) if r[1] >= 2]

    ans = 0
    while stack:
        if big and big[-1] == len(stack) - 1:
            # The last boundary is free: sweep it all the way to the end.
            ans += tail_len
            ch, ln = stack.pop()
            big.pop()
            tail_char = ch
            tail_len += ln
        else:
            # Top run has length 1; fire the nearest boundary below it.
            j = big[-1]
            ans += 1
            stack[j][1] += 1
            del stack[j + 1]
            if j + 1 < len(stack):
                if stack[j][0] == stack[j + 1][0]:
                    stack[j][1] += stack[j + 1][1]
                    del stack[j + 1]
            else:
                if stack[j][0] == tail_char:
                    tail_len += stack[j][1]
                    stack.pop()
                    big.pop()
    return ans
