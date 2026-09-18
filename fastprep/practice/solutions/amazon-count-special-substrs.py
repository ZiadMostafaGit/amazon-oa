# Run-length encode the binary string; adjacent runs of lengths a, b contribute min(a, b) balanced substrings.
def countSpecialSubstrings(s: str) -> int:
    n = len(s)
    if n < 2:
        return 0
    total = 0
    prev_run = 0
    cur_run = 1
    for i in range(1, n):
        if s[i] == s[i - 1]:
            cur_run += 1
        else:
            total += prev_run if prev_run < cur_run else cur_run
            prev_run = cur_run
            cur_run = 1
    total += prev_run if prev_run < cur_run else cur_run
    return total
