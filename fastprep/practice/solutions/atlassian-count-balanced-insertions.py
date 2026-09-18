# Prefix-balance scan: an insertion at index i works iff the prefix minimum stays valid before i and the suffix minimum tolerates the shift after i.
def countBalancedInsertions(s: str) -> int:
    n = len(s)
    pre = [0] * (n + 1)
    for i, ch in enumerate(s):
        pre[i + 1] = pre[i] + (1 if ch == '(' else -1)
    total = pre[n]
    if total == -1:
        need = -1  # inserting '(' shifts later prefixes up by 1
    elif total == 1:
        need = 1   # inserting ')' shifts later prefixes down by 1
    else:
        return 0
    suf_min = [0] * (n + 1)
    suf_min[n] = pre[n]
    for k in range(n - 1, -1, -1):
        suf_min[k] = pre[k] if pre[k] < suf_min[k + 1] else suf_min[k + 1]
    ans = 0
    run_min = pre[0]
    for i in range(n + 1):
        if i > 0 and pre[i] < run_min:
            run_min = pre[i]
        if run_min >= 0 and suf_min[i] >= need:
            ans += 1
    return ans
