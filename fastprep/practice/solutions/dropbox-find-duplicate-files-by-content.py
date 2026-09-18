# Hash-group paths by exact content, keep groups of size >= 2, sort inside and across groups.
from typing import List, Optional, Any
from collections import defaultdict


def findDuplicateFiles(paths: List[str], contents: List[str]) -> List[List[str]]:
    groups = defaultdict(list)
    for path, content in zip(paths, contents):
        groups[content].append(path)
    result = [sorted(g) for g in groups.values() if len(g) >= 2]
    result.sort(key=lambda g: g[0])
    return result
