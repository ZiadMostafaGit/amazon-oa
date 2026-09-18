# Single pass over runs, tracking the rightmost run with maximal length.
def solution(source: str) -> str:
    best_char = ""
    best_len = 0
    i = 0
    n = len(source)
    while i < n:
        j = i
        while j < n and source[j] == source[i]:
            j += 1
        run_len = j - i
        if run_len >= best_len:
            best_len = run_len
            best_char = source[i]
        i = j
    if best_len == 0:
        return ""
    return best_char + str(best_len)
