# Single pass over runs of equal characters, keeping the rightmost maximal run.
def longestSameCharacterSubstring(source: str) -> str:
    best_char = source[0]
    best_len = 0
    run_len = 0
    prev = ''
    for ch in source:
        run_len = run_len + 1 if ch == prev else 1
        prev = ch
        if run_len >= best_len:  # >= keeps the rightmost run on ties
            best_len = run_len
            best_char = ch
    return best_char + str(best_len)
