# Backward feasibility DP over (last char, run length), then a forward greedy picking 'a' when still feasible.
def solution(S: str) -> str:
    n = len(S)
    # states: 0 = nothing yet, 1 = ...a, 2 = ...aa, 3 = ...b, 4 = ...bb
    def step(state: int, c: str) -> int:
        if c == 'a':
            if state == 1:
                return 2
            if state == 2:
                return -1
            return 1
        else:
            if state == 3:
                return 4
            if state == 4:
                return -1
            return 3

    # feasible[i][state]: positions i..n-1 can be completed
    feasible = [[False] * 5 for _ in range(n + 1)]
    for st in range(5):
        feasible[n][st] = True
    for i in range(n - 1, -1, -1):
        ch = S[i]
        choices = ('a', 'b') if ch == '?' else (ch,)
        row = feasible[i]
        nxt = feasible[i + 1]
        for st in range(5):
            ok = False
            for c in choices:
                ns = step(st, c)
                if ns != -1 and nxt[ns]:
                    ok = True
                    break
            row[st] = ok

    res = []
    state = 0
    for i in range(n):
        ch = S[i]
        choices = ('a', 'b') if ch == '?' else (ch,)
        for c in choices:
            ns = step(state, c)
            if ns != -1 and feasible[i + 1][ns]:
                res.append(c)
                state = ns
                break
        else:
            return ""
    return "".join(res)
