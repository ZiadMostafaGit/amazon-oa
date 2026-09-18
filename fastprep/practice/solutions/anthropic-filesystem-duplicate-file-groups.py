# Hash-map grouping: bucket paths by exact file content, keep buckets of size >= 2, then sort.
from typing import List, Optional, Any


def findDuplicateFileGroups(paths: List[str], contents: List[str]) -> List[List[str]]:
    buckets = {}
    for path, content in zip(paths, contents):
        buckets.setdefault(content, []).append(path)
    groups = [sorted(group) for group in buckets.values() if len(group) >= 2]
    groups.sort(key=lambda g: g[0])
    return groups
