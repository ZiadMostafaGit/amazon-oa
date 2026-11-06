def countTransactionSequences(startShares: int, targetShares: int, maxTransactions: int) -> int:
    top = startShares + maxTransactions + 1
    cur = [0] * (top + 1)
    cur[startShares] = 1
    total = cur[targetShares] if targetShares <= top else 0
    for _ in range(maxTransactions):
        nxt = [0] * (top + 1)
        for h in range(top + 1):
            c = cur[h]
            if c:
                if h + 1 <= top:
                    nxt[h + 1] += c
                if h > 0:
                    nxt[h - 1] += c
        cur = nxt
        if targetShares <= top:
            total += cur[targetShares]
    return total
