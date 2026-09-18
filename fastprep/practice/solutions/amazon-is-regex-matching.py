# Tokenize regex into char/group tokens with star flags, then memoized DP matching.
from typing import List, Optional, Any
from functools import lru_cache


def _parse(regex: str):
    tokens = []
    i = 0
    n = len(regex)
    while i < n:
        if regex[i] == '(':
            j = regex.index(')', i)
            inner = regex[i + 1:j]
            i = j + 1
            star = i < n and regex[i] == '*'
            if star:
                i += 1
            tokens.append(('g', inner, star))
        else:
            c = regex[i]
            i += 1
            star = i < n and regex[i] == '*'
            if star:
                i += 1
            tokens.append(('c', c, star))
    return tokens


def _cmatch(pc: str, sc: str) -> bool:
    return pc == '.' or pc == sc


def _gmatch(inner: str, s: str, pos: int) -> bool:
    if pos + len(inner) > len(s):
        return False
    for k, pc in enumerate(inner):
        if not _cmatch(pc, s[pos + k]):
            return False
    return True


def isRegexMatching(regex: str, arr: List[str]) -> List[str]:
    tokens = _parse(regex)
    nt = len(tokens)

    def matches(s: str) -> bool:
        ns = len(s)

        @lru_cache(maxsize=None)
        def go(ti: int, pos: int) -> bool:
            if ti == nt:
                return pos == ns
            kind, body, star = tokens[ti]
            if kind == 'c':
                if star:
                    if go(ti + 1, pos):
                        return True
                    p = pos
                    while p < ns and _cmatch(body, s[p]):
                        p += 1
                        if go(ti + 1, p):
                            return True
                    return False
                return pos < ns and _cmatch(body, s[pos]) and go(ti + 1, pos + 1)
            L = len(body)
            if star:
                if L == 0:
                    return go(ti + 1, pos)
                p = pos
                while True:
                    if go(ti + 1, p):
                        return True
                    if not _gmatch(body, s, p):
                        return False
                    p += L
            if not _gmatch(body, s, pos):
                return False
            return go(ti + 1, pos + L)

        res = go(0, 0)
        go.cache_clear()
        return res

    return ["YES" if matches(s) else "NO" for s in arr]
