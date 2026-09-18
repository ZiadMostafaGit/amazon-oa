# Brute force: scan the next 1440 minutes with wraparound, return the first palindromic HHMM.
def solve(time: str) -> str:
    hh, mm = time.split(":")
    cur = int(hh) * 60 + int(mm)
    for step in range(1, 1441):
        t = (cur + step) % 1440
        h, m = divmod(t, 60)
        s = "%02d%02d" % (h, m)
        if s[0] == s[3] and s[1] == s[2]:
            return "%02d:%02d" % (h, m)
    return time
