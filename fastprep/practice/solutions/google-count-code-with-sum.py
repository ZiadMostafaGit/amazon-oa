# DP over four digit positions counting compositions with digits 0..9.
def googleCountCodeWithSum(S: int) -> int:
    counts = [1] + [0] * S
    for _ in range(4):
        nxt = [0] * (S + 1)
        for total, c in enumerate(counts):
            if not c:
                continue
            for d in range(10):
                if total + d > S:
                    break
                nxt[total + d] += c
        counts = nxt
    return counts[S]
