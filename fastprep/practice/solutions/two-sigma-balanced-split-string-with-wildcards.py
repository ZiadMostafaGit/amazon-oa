# Prefix counts of each bracket: a half is rearrangeable iff wildcards cover both imbalances with an even remainder.


def countBalancedSplits(s: str) -> int:
    n = len(s)
    # prefix counts of '(', ')', '[', ']', '?'
    a = b = c = d = q = 0
    total_a = s.count('(')
    total_b = s.count(')')
    total_c = s.count('[')
    total_d = s.count(']')
    total_q = s.count('?')

    def feasible(pa, pb, pc, pd, pq):
        need = abs(pa - pb) + abs(pc - pd)
        rest = pq - need
        return rest >= 0 and rest % 2 == 0

    ans = 0
    for i in range(n - 1):
        ch = s[i]
        if ch == '(':
            a += 1
        elif ch == ')':
            b += 1
        elif ch == '[':
            c += 1
        elif ch == ']':
            d += 1
        else:
            q += 1
        if feasible(a, b, c, d, q) and feasible(total_a - a, total_b - b, total_c - c, total_d - d, total_q - q):
            ans += 1
    return ans
