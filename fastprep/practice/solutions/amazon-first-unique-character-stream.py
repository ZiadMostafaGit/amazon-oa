# Frequency map plus a queue of candidates; pop stale fronts to get the current first unique char.
from collections import deque


def solve(stream: str) -> str:
    freq = {}
    q = deque()
    out = []
    for ch in stream:
        freq[ch] = freq.get(ch, 0) + 1
        q.append(ch)
        while q and freq[q[0]] > 1:
            q.popleft()
        out.append(q[0] if q else '#')
    return ''.join(out)
