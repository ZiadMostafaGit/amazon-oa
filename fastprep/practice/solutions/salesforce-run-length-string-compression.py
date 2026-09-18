# Single linear scan over maximal runs, appending the character and the run length when it exceeds one.
def compressString(s: str) -> str:
    if not s:
        return ""
    parts = []
    run_char = s[0]
    run_len = 1
    for ch in s[1:]:
        if ch == run_char:
            run_len += 1
        else:
            parts.append(run_char)
            if run_len > 1:
                parts.append(str(run_len))
            run_char = ch
            run_len = 1
    parts.append(run_char)
    if run_len > 1:
        parts.append(str(run_len))
    return "".join(parts)
