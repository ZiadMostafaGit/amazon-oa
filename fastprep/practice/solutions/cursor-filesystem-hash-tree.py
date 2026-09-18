# Build the parent/child tree, then hash bottom-up by descending depth with 64-bit FNV-1a.
from typing import List, Optional, Any

_MASK = (1 << 64) - 1
_BASIS = 0xcbf29ce484222325
_PRIME = 0x100000001b3


def _fnv1a(data: bytes) -> str:
    h = _BASIS
    for b in data:
        h = ((h ^ b) * _PRIME) & _MASK
    return format(h, '016x')


def hashFileSystem(paths: List[str], types: List[str], contents: List[str]) -> List[str]:
    n = len(paths)
    children = {p: [] for p in paths}
    kind = {}
    body = {}
    for i in range(n):
        p = paths[i]
        kind[p] = types[i]
        body[p] = contents[i]
        if p != '/':
            parent = p.rsplit('/', 1)[0]
            if parent == '':
                parent = '/'
            name = p.rsplit('/', 1)[1]
            if parent in children:
                children[parent].append((name, p))
    for p in children:
        children[p].sort()

    # Deepest paths first so every child is hashed before its parent.
    order = sorted(paths, key=lambda p: 0 if p == '/' else p.count('/'), reverse=True)
    hashes = {}
    for p in order:
        if kind[p] == 'FILE':
            hashes[p] = _fnv1a(body[p].encode('utf-8'))
        else:
            joined = ''.join(hashes[c] for _, c in children[p])
            hashes[p] = _fnv1a(joined.encode('ascii'))
    return [p + '=' + hashes[p] for p in sorted(paths)]
