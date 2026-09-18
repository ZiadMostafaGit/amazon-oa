# BFS over the set of distinct retained parenthesis strings (n <= 16), applying each digit as d single deletions with dedup.
def solve(s: str) -> bool:
    states = {""}
    for ch in s:
        if ch == '(' or ch == ')':
            states = {t + ch for t in states}
        elif ch.isdigit():
            d = int(ch)
            for _ in range(d):
                nxt = set()
                for t in states:
                    for i in range(len(t)):
                        nxt.add(t[:i] + t[i + 1:])
                states = nxt
                if not states:
                    return False
        # any other character is ignored
        if not states:
            return False
    for t in states:
        bal = 0
        ok = True
        for c in t:
            bal += 1 if c == '(' else -1
            if bal < 0:
                ok = False
                break
        if ok and bal == 0:
            return True
    return False
