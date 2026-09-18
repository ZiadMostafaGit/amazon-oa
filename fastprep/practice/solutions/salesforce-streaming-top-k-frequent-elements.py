# Incremental top-k: only the arriving value's rank can improve, so patch the maintained list.
from typing import List, Optional, Any


def topKAfterEach(stream: List[int], k: int) -> List[List[int]]:
    cnt = {}
    top = []          # values currently in the top k, sorted by (-count, value)
    inTop = set()
    res = []
    for v in stream:
        cnt[v] = cnt.get(v, 0) + 1
        if v not in inTop:
            if len(top) < k:
                top.append(v)
                inTop.add(v)
            else:
                worst = top[-1]
                if (-cnt[v], v) < (-cnt[worst], worst):
                    top[-1] = v
                    inTop.discard(worst)
                    inTop.add(v)
        top.sort(key=lambda x: (-cnt[x], x))
        res.append(list(top))
    return res
