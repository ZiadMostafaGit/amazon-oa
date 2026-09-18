# Approach: signature -> multiset index with a lazy max-heap keyed by (-size, signature) for O(log n) queries.
import heapq
from typing import Dict, List


def largestAnagramGroups(operations: List[List[str]]) -> List[List[str]]:
    groups: Dict[str, Dict[str, int]] = {}
    sizes: Dict[str, int] = {}
    heap: List = []
    out: List[List[str]] = []

    for op in operations:
        kind = op[0]
        if kind == "add":
            word = op[1]
            sig = "".join(sorted(word))
            bucket = groups.get(sig)
            if bucket is None:
                bucket = {}
                groups[sig] = bucket
                sizes[sig] = 0
            bucket[word] = bucket.get(word, 0) + 1
            sizes[sig] += 1
            heapq.heappush(heap, (-sizes[sig], sig))
        elif kind == "remove":
            word = op[1]
            sig = "".join(sorted(word))
            bucket = groups.get(sig)
            if bucket and bucket.get(word, 0) > 0:
                bucket[word] -= 1
                if bucket[word] == 0:
                    del bucket[word]
                sizes[sig] -= 1
                if sizes[sig] == 0:
                    del sizes[sig]
                    del groups[sig]
                else:
                    heapq.heappush(heap, (-sizes[sig], sig))
        else:
            while heap and sizes.get(heap[0][1], 0) != -heap[0][0]:
                heapq.heappop(heap)
            if not heap:
                out.append([])
                continue
            sig = heap[0][1]
            row: List[str] = []
            for w in sorted(groups[sig]):
                row.extend([w] * groups[sig][w])
            out.append(row)
    return out
