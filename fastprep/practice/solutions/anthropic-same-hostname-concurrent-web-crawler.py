# Level-synchronous BFS over the page graph, each frontier fetched by a pool of workerCount threads.
from typing import List, Optional, Any
from concurrent.futures import ThreadPoolExecutor
import threading


def _strip_fragment(url: str) -> str:
    i = url.find('#')
    return url if i == -1 else url[:i]


def _hostname(url: str) -> str:
    i = url.find('://')
    rest = url[i + 3:] if i != -1 else url
    end = len(rest)
    for ch in ('/', '?'):
        j = rest.find(ch)
        if j != -1 and j < end:
            end = j
    return rest[:end]


def crawlSameHostname(startUrl: str, pageUrls: List[str], linkLists: List[str], workerCount: int) -> List[str]:
    graph = {}
    for page, links in zip(pageUrls, linkLists):
        graph[_strip_fragment(page)] = [_strip_fragment(u) for u in links.split() if u]

    start = _strip_fragment(startUrl)
    host = _hostname(start)

    lock = threading.Lock()
    visited = {start}
    frontier = [start]

    def fetch(url):
        return graph.get(url, [])

    workers = max(1, int(workerCount))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        while frontier:
            results = list(pool.map(fetch, frontier))
            nxt = []
            for links in results:
                for link in links:
                    if _hostname(link) != host:
                        continue
                    with lock:
                        if link in visited:
                            continue
                        visited.add(link)
                    nxt.append(link)
            frontier = nxt

    return sorted(visited)
