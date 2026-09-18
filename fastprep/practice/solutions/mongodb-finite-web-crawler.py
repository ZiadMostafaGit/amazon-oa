# BFS over a finite URL graph using a set of known URLs and a discovered set.
from typing import List, Optional, Any
from collections import deque


def crawlPages(urls: List[str], links: List[List[str]], startUrl: str) -> List[str]:
    index = {u: i for i, u in enumerate(urls)}
    if startUrl not in index:
        return []
    order = [startUrl]
    seen = {startUrl}
    q = deque([index[startUrl]])
    while q:
        i = q.popleft()
        for link in links[i]:
            j = index.get(link)
            if j is not None and link not in seen:
                seen.add(link)
                order.append(link)
                q.append(j)
    return order
