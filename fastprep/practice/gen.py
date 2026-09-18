"""Generate random inputs for a problem from its declared types.

The bank gives every input a type (`int[]`, `String[][]`, `TreeNode`, ...) but
no generator and no constraints in machine-readable form, so these inputs are
type-correct and nothing more: some will violate a problem's rules ("all
distinct", "already sorted", "a valid tiling"). That is handled downstream -
an input the reference solution rejects is discarded rather than counted, so a
disagreement is only ever reported on an input the reference itself accepted.

Shapes stay small on purpose: the point is to find a disagreement quickly, not
to benchmark.
"""

from __future__ import annotations

import parsing

WORDS = ["a", "ab", "abc", "b", "bc", "x", "yz", "cat", "dog", "red", "blue", "0", "1", "10"]


def _scalar(rng, t: str, size: int):
    if t in parsing.INT_TYPES:
        return rng.randint(-size, size)
    if t in parsing.REAL_TYPES:
        return round(rng.uniform(-size, size), 3)
    if t in parsing.BOOL_TYPES:
        return rng.random() < 0.5
    if t in parsing.CHAR_TYPES:
        return rng.choice("abcxyz01")
    if t in parsing.STR_TYPES:
        return rng.choice(WORDS)
    return rng.randint(0, size)


def value(rng, typ: str, size: int = 6):
    """One random value of the declared type, as a plain Python structure."""
    t = (typ or "").strip()
    if t == "TreeNode":
        n = rng.randint(0, size)
        out = []
        for i in range(n):
            # a null only after the root, so the encoding stays well-formed
            out.append(None if (i and rng.random() < 0.25) else rng.randint(-size, size))
        return out
    if t == "ListNode":
        return [rng.randint(-size, size) for _ in range(rng.randint(0, size))]
    if t == "ListNode[]":
        return [[rng.randint(-size, size) for _ in range(rng.randint(0, 4))]
                for _ in range(rng.randint(0, 3))]
    el = parsing.element_type(t)
    if el is not None:
        n = rng.randint(0, max(1, size if parsing.depth(t) == 1 else 3))
        return [value(rng, el, size) for _ in range(n)]
    return _scalar(rng, t, size)


def args_for(inputs: list, rng, size: int = 6) -> list:
    """One argument list for a problem, from its first example's declared types."""
    return [value(rng, i.get("type"), size) for i in inputs]
