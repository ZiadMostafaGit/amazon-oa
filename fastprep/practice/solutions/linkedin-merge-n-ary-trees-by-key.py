# Merged node set == union of root-to-node key paths, so build each tree's paths and sort the union.
from typing import List, Optional, Any


def _paths(keys: List[str], parents: List[int]) -> List[str]:
    out = []
    for i, key in enumerate(keys):
        p = parents[i]
        out.append(key if p < 0 else out[p] + "/" + key)
    return out


def mergeNaryTrees(keys1: List[str], parents1: List[int], keys2: List[str], parents2: List[int]) -> List[str]:
    merged = set(_paths(keys1, parents1))
    merged.update(_paths(keys2, parents2))
    return sorted(merged)
