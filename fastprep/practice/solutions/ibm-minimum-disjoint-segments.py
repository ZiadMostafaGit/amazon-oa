# Greedy: extend the current segment until a character repeats, then start a new one.
def minimumDisjointSegments(s: str) -> int:
    if not s:
        return 0
    count = 1
    seen = set()
    for ch in s:
        if ch in seen:
            count += 1
            seen = {ch}
        else:
            seen.add(ch)
    return count
