# Memoize each transform prefix (as a tuple key) so shared prefixes are computed once.
from typing import List, Optional, Any, Tuple


def _rotate_cw(img):
    h = len(img)
    w = len(img[0]) if h else 0
    return [[img[h - 1 - r][c] for r in range(h)] for c in range(w)]


def _flip_h(img):
    return [row[::-1] for row in img]


def _invert(img):
    return [[255 - v for v in row] for row in img]


def _enlarge(img):
    out = []
    for row in img:
        big = []
        for v in row:
            big.append(v)
            big.append(v)
        out.append(big)
        out.append(list(big))
    return out


def _shrink(img):
    h = len(img)
    w = len(img[0]) if h else 0
    out = []
    for r in range(0, h, 2):
        row = []
        a = img[r]
        b = img[r + 1]
        for c in range(0, w, 2):
            row.append((a[c] + a[c + 1] + b[c] + b[c + 1]) // 4)
        out.append(row)
    return out


_OPS = {
    "ROTATE_CW": _rotate_cw,
    "FLIP_HORIZONTAL": _flip_h,
    "INVERT": _invert,
    "ENLARGE_2X": _enlarge,
    "SHRINK_2X": _shrink,
}


def runCachedImagePipelines(image: List[List[int]], pipelines: List[List[str]]) -> List[str]:
    cache = {(): [list(row) for row in image]}
    steps = 0

    def compute(prefix: Tuple[str, ...]):
        nonlocal steps
        if prefix in cache:
            return cache[prefix]
        base = compute(prefix[:-1])
        result = _OPS[prefix[-1]](base)
        cache[prefix] = result
        steps += 1
        return result

    finals = []
    for pipeline in pipelines:
        img = compute(tuple(pipeline))
        finals.append("/".join(",".join(str(v) for v in row) for row in img))

    return ["steps=" + str(steps)] + finals
