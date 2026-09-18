# Approach: heap-based k-way merge over paged fetches, emitting each id once via last-written dedup.
import heapq
from typing import List, Optional, Any


def mergePagedSources(sources: List[List[int]], pageSize: int) -> List[int]:
    if not sources:
        return []

    # offsets[i] = next record index to fetch from source i
    offsets = [0] * len(sources)
    pages = [None] * len(sources)      # current in-memory page per source
    page_pos = [0] * len(sources)      # cursor inside the current page

    def fetch(i: int) -> bool:
        """Load the next page of source i; return False when the source is exhausted."""
        src = sources[i]
        start = offsets[i]
        if start >= len(src):
            pages[i] = None
            return False
        end = min(start + pageSize, len(src))
        pages[i] = src[start:end]
        page_pos[i] = 0
        offsets[i] = end
        return True

    heap = []
    for i in range(len(sources)):
        if fetch(i):
            heapq.heappush(heap, (pages[i][0], i))

    out = []
    last = None
    while heap:
        val, i = heapq.heappop(heap)
        if last is None or val != last:
            out.append(val)
            last = val
        # advance source i by one record, refilling its page when drained
        page_pos[i] += 1
        if page_pos[i] >= len(pages[i]):
            if not fetch(i):
                continue
        heapq.heappush(heap, (pages[i][page_pos[i]], i))
    return out
