# Single linear scan over runs, keeping the rightmost run of maximal length.
def solution(source: str) -> str:
    best_char = source[0]
    best_len = 0
    i = 0
    n = len(source)
    while i < n:
        j = i
        while j < n and source[j] == source[i]:
            j += 1
        run = j - i
        if run >= best_len:          # >= keeps the rightmost maximum
            best_len = run
            best_char = source[i]
        i = j
    return best_char + str(best_len)
