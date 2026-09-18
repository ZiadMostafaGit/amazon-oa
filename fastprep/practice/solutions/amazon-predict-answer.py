# Monotonic stacks give previous/next strictly-smaller indices; pick the closer one, ties go to the earlier day.
from typing import List, Optional, Any


def predictAnswer(stockData: List[int], queries: List[int]) -> List[int]:
    n = len(stockData)
    prev = [-1] * n
    nxt = [-1] * n

    stack = []
    for i in range(n):
        v = stockData[i]
        while stack and stockData[stack[-1]] >= v:
            stack.pop()
        prev[i] = stack[-1] if stack else -1
        stack.append(i)

    stack = []
    for i in range(n - 1, -1, -1):
        v = stockData[i]
        while stack and stockData[stack[-1]] >= v:
            stack.pop()
        nxt[i] = stack[-1] if stack else -1
        stack.append(i)

    out = []
    for q in queries:
        i = q - 1
        p = prev[i]
        f = nxt[i]
        if p == -1 and f == -1:
            out.append(-1)
        elif p == -1:
            out.append(f + 1)
        elif f == -1:
            out.append(p + 1)
        else:
            # tie in distance -> smaller day number, i.e. the earlier index
            out.append((p + 1) if (i - p) <= (f - i) else (f + 1))
    return out
