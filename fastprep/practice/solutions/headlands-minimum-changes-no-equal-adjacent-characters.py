# Greedy over maximal runs of equal characters: a run of length L needs L // 2 replacements.
def minimumChangesForDistinctAdjacentCharacters(s: str) -> int:
    total = 0
    run = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            run += 1
        else:
            total += run // 2
            run = 1
    total += run // 2
    return total
