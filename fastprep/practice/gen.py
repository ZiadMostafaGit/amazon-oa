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


# --------------------------------------------------------------------------
# mutation
# --------------------------------------------------------------------------
# Pure type-driven generation is valid but often meaningless: a problem whose
# input is a list of command words ("ENCODE", "DECODE") gets random nouns and
# the reference just returns nothing. Mutating the problem's OWN example keeps
# its vocabulary and structure, so the variants exercise the same code paths.

def _scalars(value, out: list) -> list:
    if isinstance(value, list):
        for v in value:
            _scalars(v, out)
    elif value is not None:
        out.append(value)
    return out


def mutate(value, rng, pool=None, depth_left: int = 4):
    """A variant of one example value, drawing new material from the example."""
    if pool is None:
        pool = _scalars(value, []) or [0, 1]

    if isinstance(value, list):
        out = list(value)
        for _ in range(rng.randint(1, 3)):
            if not out or depth_left <= 0:
                break
            roll = rng.random()
            if roll < 0.3 and len(out) > 1:                 # drop one
                out.pop(rng.randrange(len(out)))
            elif roll < 0.5:                                # duplicate one
                out.insert(rng.randrange(len(out) + 1), out[rng.randrange(len(out))])
            elif roll < 0.7:                                # reorder
                rng.shuffle(out)
            else:                                           # mutate one element
                i = rng.randrange(len(out))
                out[i] = mutate(out[i], rng, pool, depth_left - 1)
        return out

    if isinstance(value, bool):
        return not value if rng.random() < 0.5 else value
    if isinstance(value, int):
        return rng.choice([value, value + rng.randint(-3, 3), -value, 0,
                           rng.choice([p for p in pool if isinstance(p, int)] or [value])])
    if isinstance(value, float):
        return round(rng.choice([value, value + rng.uniform(-2, 2), 0.0]), 3)
    if isinstance(value, str):
        # Strings carry meaning, and the meaning differs by shape. A short
        # string among several distinct ones is a TOKEN - a command, a key, an
        # enum - and editing its characters invents something the problem never
        # allows ("empty" -> "epty"), so tokens are only ever swapped for other
        # tokens the example already used. A single long string is DATA, and
        # character edits are exactly what you want.
        words = [p for p in pool if isinstance(p, str)] or [value]
        vocabulary = {w for w in words if len(w) <= 12}
        looks_like_a_token = len(value) <= 12 and len(vocabulary) >= 2
        if looks_like_a_token:
            return rng.choice(sorted(vocabulary))
        roll = rng.random()
        if roll < 0.4 and len(value) > 1:                   # drop a character
            i = rng.randrange(len(value))
            return value[:i] + value[i + 1:]
        if roll < 0.7 and len(value) > 1:                   # repeat one, making a run
            i = rng.randrange(len(value))
            return value[:i] + value[i] + value[i:]
        if roll < 0.85:
            return rng.choice(words)
        return value
    return value


def variant_of(example_args: list, rng) -> list:
    """Mutate every argument of one example, keeping its shape and vocabulary."""
    pool = []
    for a in example_args:
        _scalars(a, pool)
    return [mutate(a, rng, pool or None) for a in example_args]
