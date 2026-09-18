# Approach: greedy max-heap on remaining counts (ties by smallest letter), never reusing the previous char.
import heapq


def solve(s: str) -> str:
    counts = [0] * 26
    for ch in s:
        counts[ord(ch) - 97] += 1
    n = len(s)
    if n == 0:
        return ""
    if max(counts) > (n + 1) // 2:
        return ""
    heap = [(-counts[c], c) for c in range(26) if counts[c] > 0]
    heapq.heapify(heap)
    out = []
    prev = None  # (negcount, char) held back for one step
    while heap:
        negc, c = heapq.heappop(heap)
        out.append(chr(c + 97))
        negc += 1
        if prev is not None:
            heapq.heappush(heap, prev)
            prev = None
        if negc < 0:
            prev = (negc, c)
    if prev is not None:
        return ""
    return "".join(out)
