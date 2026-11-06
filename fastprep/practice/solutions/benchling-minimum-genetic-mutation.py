from typing import List, Optional, Any
from collections import deque


def minMutation(startGene: str, endGene: str, bank: List[str]) -> int:
    if startGene == endGene:
        return 0
    valid = set(bank)
    if endGene not in valid:
        return -1
    seen = {startGene}
    q = deque([(startGene, 0)])
    while q:
        gene, d = q.popleft()
        for i in range(len(gene)):
            for ch in "ACGT":
                if ch == gene[i]:
                    continue
                nxt = gene[:i] + ch + gene[i + 1:]
                if nxt in valid and nxt not in seen:
                    if nxt == endGene:
                        return d + 1
                    seen.add(nxt)
                    q.append((nxt, d + 1))
    return -1
