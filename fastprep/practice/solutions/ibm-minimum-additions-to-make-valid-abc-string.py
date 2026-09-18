# Greedy cycle scan: walk "abc" repeatedly, charging one insertion for every letter the word does not supply.
def addMinimum(word: str) -> int:
    n = len(word)
    i = 0
    added = 0
    while i < n:
        for ch in "abc":
            if i < n and word[i] == ch:
                i += 1
            else:
                added += 1
    return added
