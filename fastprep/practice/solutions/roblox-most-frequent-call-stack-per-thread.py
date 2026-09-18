# Hash counting: tally (thread, path) pairs, then per thread pick max count with lexicographically smallest path as tie-break.
from typing import List, Optional, Any


def mostFrequentCallStackPerThread(samples: List[str]) -> List[str]:
    per_thread = {}
    for record in samples:
        tid, _, path = record.partition("|")
        counts = per_thread.get(tid)
        if counts is None:
            counts = {}
            per_thread[tid] = counts
        counts[path] = counts.get(path, 0) + 1

    result = []
    for tid in sorted(per_thread):
        best_path = None
        best_count = 0
        for path, count in per_thread[tid].items():
            if count > best_count or (count == best_count and path < best_path):
                best_path = path
                best_count = count
        result.append("%s|%s|%d" % (tid, best_path, best_count))
    return result
