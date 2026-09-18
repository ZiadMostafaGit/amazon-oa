# Union-Find over synonym pairs, then positional comparison of the two sentences.
from typing import List, Optional, Any


def areSentencesEquivalent(firstSentence: List[str], secondSentence: List[str], synonymPairs: List[List[str]]) -> bool:
    if len(firstSentence) != len(secondSentence):
        return False

    parent = {}

    def find(x: str) -> str:
        parent.setdefault(x, x)
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    for pair in synonymPairs:
        a, b = pair[0], pair[1]
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for a, b in zip(firstSentence, secondSentence):
        if a == b:
            continue
        if a not in parent or b not in parent:
            return False
        if find(a) != find(b):
            return False
    return True
