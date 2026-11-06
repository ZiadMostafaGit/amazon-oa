# Trie of sentences with a frequency at each sentence end. Keep a pointer to the current query's node: each
# typed character is one child step, and a DFS below that node collects the candidates to rank.
from typing import List

_END = "#"


def autocomplete(sentences: List[str], times: List[int], inputs: str) -> List[List[str]]:
    root = {}

    def add(s, t):
        node = root
        for ch in s:
            node = node.setdefault(ch, {})
        node[_END] = node.get(_END, 0) + t

    for s, t in zip(sentences, times):
        add(s, t)

    def collect(node, prefix):
        found = []
        stack = [(node, prefix)]
        while stack:
            cur, text = stack.pop()
            for key, child in cur.items():
                if key == _END:
                    found.append((-child, text))
                else:
                    stack.append((child, text + key))
        found.sort()
        return [text for _, text in found[:3]]

    out = []
    query = []
    node = root
    for ch in inputs:
        if ch == "#":
            add("".join(query), 1)
            query = []
            node = root
            out.append([])
            continue
        query.append(ch)
        if node is not None:
            node = node.get(ch)
        out.append(collect(node, "".join(query)) if node is not None else [])
    return out
