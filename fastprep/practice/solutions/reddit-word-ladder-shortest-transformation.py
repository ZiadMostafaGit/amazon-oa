# Bidirectional BFS over one-letter mutations of the dictionary words.
from typing import List, Optional, Any


def ladderLength(beginWord: str, endWord: str, wordList: List[str]) -> int:
    words = set(wordList)
    if endWord not in words:
        return 0
    letters = "abcdefghijklmnopqrstuvwxyz"
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
                prefix, suffix = word[:i], word[i + 1:]
                for c in letters:
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
