def metaReplaceConsonant(message: str, n: int) -> str:
    cons = "bcdfghjklmnpqrstvwxyz"
    nxt = {cons[i]: cons[(i + 1) % len(cons)] for i in range(len(cons))}
    out = []
    seen = 0
    for ch in message:
        low = ch.lower()
        if low in nxt:
            seen += 1
            if seen % n == 0:
                rep = nxt[low]
                ch = rep.upper() if ch.isupper() else rep
        out.append(ch)
    return "".join(out)
