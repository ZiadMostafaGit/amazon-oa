def countEqualDistinctPartitions(value: str) -> int:
    MOD = 10**9 + 7
    n = len(value)
    # pre[d][i] = sum of ways[d][0..i-1], ways[d][j] = valid partitions of value[:j]
    # where every part has exactly d distinct characters.
    pre = [[0] * (n + 2) for _ in range(27)]
    for d in range(1, 27):
        pre[d][1] = 1  # ways[d][0] = 1
    last = []  # positions of last occurrences, most recent first
    pos = {}
    ans = 0
    for i in range(1, n + 1):
        c = value[i - 1]
        if c in pos:
            last.remove(pos[c])
        pos[c] = i - 1
        last.insert(0, i - 1)
        m = len(last)
        for d in range(1, m + 1):
            hi = last[d - 1]                       # j <= hi
            lo = last[d] if d < m else -1          # j > lo
            w = (pre[d][hi + 1] - pre[d][lo + 1]) % MOD
            pre[d][i + 1] = (pre[d][i] + w) % MOD
            if i == n:
                ans += w
        for d in range(m + 1, 27):
            pre[d][i + 1] = pre[d][i]
    return ans % MOD
