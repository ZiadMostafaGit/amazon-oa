# Bidirectional BFS over the dictionary, generating one-character neighbors.
from typing import List, Optional, Any
from string import ascii_lowercase


def ladderLength(beginWord: str, endWord: str, wordList: List[str]) -> int:
    words = set(wordList)
    if endWord not in words:
        return 0
    if beginWord == endWord:
        return 1
    front = {beginWord}
    back = {endWord}
    words.discard(beginWord)
    words.discard(endWord)
    steps = 1
    while front and back:
        if len(front) > len(back):
            front, back = back, front
        steps += 1
        nxt = set()
        for word in front:
            for i in range(len(word)):
                prefix = word[:i]
                suffix = word[i + 1:]
                for c in ascii_lowercase:
                    if c == word[i]:
                        continue
                    cand = prefix + c + suffix
                    if cand in back:
                        return steps
                    if cand in words:
                        words.discard(cand)
                        nxt.add(cand)
        front = nxt
    return 0
