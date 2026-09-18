# Store each cell as pre-parsed terms; each GET resolves references with an iterative DFS and a per-query memo.
from typing import List


def runSpreadsheet(operations: List[str]) -> List[int]:
    cells = {}
    out = []
    for op in operations:
        parts = op.split(None, 2)
        if parts[0] == "SET":
            name = parts[1]
            terms = []
            for tok in parts[2].split('+'):
                tok = tok.strip()
                if not tok:
                    continue
                if tok[0] in '-+0123456789':
                    terms.append(int(tok))
                else:
                    terms.append(tok)
            cells[name] = terms
        else:
            start = parts[1]
            memo = {}
            stack = [start]
            while stack:
                cur = stack[-1]
                if cur in memo:
                    stack.pop()
                    continue
                total = 0
                ready = True
                for t in cells[cur]:
                    if type(t) is int:
                        total += t
                    else:
                        v = memo.get(t)
                        if v is None:
                            stack.append(t)
                            ready = False
                        else:
                            total += v
                if ready:
                    memo[cur] = total
                    stack.pop()
            out.append(memo[start])
    return out
