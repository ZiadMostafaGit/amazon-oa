# Arrays and Contiguous Memory

> An array is not a list of values. It is a promise that element `i` lives at
> `base + i·w`, and nearly every array technique is a way of spending that
> promise — free random access — to buy something the problem wants more.

## When you reach for it

You reach for an array when the data is a **sequence whose positions mean
something**, and the operations you need are "read the `i`-th thing" and "walk
from one end to the other". That is such a common shape that the array is the
default container rather than a choice: 2023 of the problems in this bank are
tagged with it, which makes it #1 of 150 topics. Nobody decides to use an array;
you decide *not* to, and the interesting question is when.

So learn the trigger backwards — learn the four situations where the contiguous
layout is exactly wrong:

- **You insert or delete in the middle, repeatedly.** Every such operation shifts
  a suffix. A loop of them is `Θ(n²)`. That is a [[linked-list]], or a rethink.
- **You look things up by value, not by position.** "Have I seen this before?" is
  `Θ(n)` in an array and `O(1)` expected in a [[hash-tables|hash table]].
  *All Pairs with Target Sum* and *Count Cross-Array Target-Sum Pairs* are array
  problems whose whole answer is "stop scanning, build a counter".
- **You need the smallest element while items keep arriving.** That is a
  [[heap]], not a re-sorted array.
- **You push and pop at both ends.** `list.pop(0)` in Python moves every
  remaining element. Use a [[deque]].

What the array is unbeatable at is the pass. One cursor, or two, sweeping left to
right, reading each slot once, writing at most once, carrying a few scalars of
state. *Array Leader Elements* ("strictly greater than everything to its right")
is one right-to-left pass with a running maximum. *Remove Duplicates From Sorted
Array In Place* is one left-to-right pass with two cursors. *Merge Sorted Array*
is one right-to-left pass with three. The statements look unrelated; the
machinery is the same, and this chapter is about that machinery.

There is one anti-signal worth naming early. The word **"subarray"** means
contiguous and is an array problem — *Count Descending Subarrays*, *Count
Strictly Increasing Contiguous Windows*. The word **"subsequence"** means you may
skip, the count is exponential, and no cursor sweep will save you; that is
[[dynamic-programming]]. Reading the wrong one of those two words costs more
interviews than any off-by-one.

## The idea

Picture a row of boxes of equal width, starting at a known address. To reach box
`i` you do not walk: you compute `base + i·w` and arrive.

<svg viewBox="0 0 660 170" role="img" aria-label="a row of equal-width memory cells with addresses base plus i times w, and an arrow computing the address of index four directly">
  <g>
    <rect x="30" y="55" width="72" height="44" rx="3"/>
    <rect x="102" y="55" width="72" height="44" rx="3"/>
    <rect x="174" y="55" width="72" height="44" rx="3"/>
    <rect x="246" y="55" width="72" height="44" rx="3"/>
    <rect class="fill" x="318" y="55" width="72" height="44" rx="3"/>
    <rect x="390" y="55" width="72" height="44" rx="3"/>
    <rect x="462" y="55" width="72" height="44" rx="3"/>
    <text x="66" y="82" text-anchor="middle">0</text>
    <text x="138" y="82" text-anchor="middle">1</text>
    <text x="210" y="82" text-anchor="middle">2</text>
    <text x="282" y="82" text-anchor="middle">3</text>
    <text x="354" y="82" text-anchor="middle">4</text>
    <text x="426" y="82" text-anchor="middle">5</text>
    <text x="498" y="82" text-anchor="middle">6</text>
    <text x="30" y="45">base</text>
    <text x="330" y="45">base + 4w</text>
    <line x1="30" y1="112" x2="534" y2="112"/>
    <line x1="30" y1="106" x2="30" y2="118"/>
    <line x1="534" y1="106" x2="534" y2="118"/>
    <text x="150" y="134">w bytes each, no gaps, ever</text>
    <line x1="354" y1="30" x2="354" y2="50"/>
    <line x1="354" y1="50" x2="348" y2="40"/>
    <line x1="354" y1="50" x2="360" y2="40"/>
    <text x="30" y="160">one multiply, one add: every index costs the same</text>
  </g>
</svg>

Two consequences follow from that single picture, and everything else in this
chapter is downstream of them.

**There are no gaps.** Making room at position `i` means physically moving
`n - i` elements one slot right. Deleting means moving them back. The array is
fast because the elements are packed, and it is slow to edit in the middle for
exactly the same reason. You do not get to keep one without the other.

**Because access is free, the state of an algorithm can be a handful of
indices.** You never need to "hold" a sub-list; you hold its endpoints. This is
what makes `O(1)` extra space realistic for problems that look like they need a
second array.

And now the lever that turns those two facts into a technique. Suppose you want
to produce a filtered or rearranged version of the array. The obvious move is to
build a new list. The better move is to run **two cursors over the same memory**:
`r` reads, `w` writes, and `w` never gets ahead of `r`.

<svg viewBox="0 0 660 185" role="img" aria-label="one array with a write cursor trailing behind a read cursor, kept prefix on the left and untouched tail on the right">
  <g>
    <rect class="fill" x="30" y="60" width="60" height="44" rx="3"/>
    <rect class="fill" x="90" y="60" width="60" height="44" rx="3"/>
    <rect class="fill" x="150" y="60" width="60" height="44" rx="3"/>
    <rect x="210" y="60" width="60" height="44" rx="3"/>
    <rect x="270" y="60" width="60" height="44" rx="3"/>
    <rect x="330" y="60" width="60" height="44" rx="3"/>
    <rect x="390" y="60" width="60" height="44" rx="3"/>
    <rect x="450" y="60" width="60" height="44" rx="3"/>
    <rect x="510" y="60" width="60" height="44" rx="3"/>
    <text x="120" y="50" text-anchor="middle">kept, in order</text>
    <text x="460" y="50" text-anchor="middle">original, untouched</text>
    <line x1="240" y1="130" x2="240" y2="108"/>
    <text x="240" y="148" text-anchor="middle">w</text>
    <line x1="360" y1="130" x2="360" y2="108"/>
    <text x="360" y="148" text-anchor="middle">r</text>
    <line x1="245" y1="140" x2="355" y2="140"/>
    <text x="300" y="175" text-anchor="middle">scratch: already read, safe to clobber</text>
  </g>
</svg>

The region between `w` and `r` is the whole trick. It is memory whose original
contents have already been consumed and whose new contents are not yet decided —
free workspace that grows exactly as fast as you throw elements away. That is why
in-place compaction needs no buffer: the buffer is the garbage you created.

## Worked by hand

Deduplicate a sorted array in place, the shape of *Deduplicate a Sorted Array In
Place* and *Remove Duplicates From Sorted Array In Place*. Keep an element when
it differs from the last one kept.

`a = [1, 1, 2, 3, 3, 3, 5]`, `n = 7`. Start `r = 0`, `w = 0`. The test is
`w == 0 or a[r] != a[w-1]`.

| r | `a[r]` | last kept `a[w-1]` | keep? | write | array after | w |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | — | yes | `a[0] = 1` | `[1,1,2,3,3,3,5]` | 1 |
| 1 | 1 | 1 | no | — | `[1,1,2,3,3,3,5]` | 1 |
| 2 | 2 | 1 | yes | `a[1] = 2` | `[1,2,2,3,3,3,5]` | 2 |
| 3 | 3 | 2 | yes | `a[2] = 3` | `[1,2,3,3,3,3,5]` | 3 |
| 4 | 3 | 3 | no | — | `[1,2,3,3,3,3,5]` | 3 |
| 5 | 3 | 3 | no | — | `[1,2,3,3,3,3,5]` | 3 |
| 6 | 5 | 3 | yes | `a[3] = 5` | `[1,2,3,5,3,3,5]` | 4 |

Return `w = 4`. The answer is `a[0:4] = [1, 2, 3, 5]`, and the tail
`[3, 3, 5]` is rubbish that the caller must not look at.

Four things in that table are invisible in the code.

**The function cannot return an array.** It returns a length. The array object
still has seven slots — Python could shrink it, C could not, and the problems
phrase it as "return the new length" precisely because the contiguous block is
fixed. Every caller that writes `len(a)` afterwards is wrong.

**At step 3 we destroyed an original value.** `a[2]` was `2`; we overwrote it
with `3`. By then `2` had already been copied to `a[1]`, so nothing was lost —
but note what it means: *everything behind the read cursor is scratch*. Any logic
that wants to look back at "the element two positions ago" is reading a value
that may no longer exist.

**Except for exactly one slot.** At the moment the loop reads `a[r]`, the value
in `a[r-1]` is still original. Index `j` is only ever written during the step
where `w == j`, and since `w <= r` always, that step has `r >= j`; the only way to
write index `r-1` before step `r` is at step `r-1` with `w = r-1`, which stores
`a[r-1]` into itself. One slot of grace, no more. A dedup written as
`a[r] != a[r-1]` therefore also works here — and the same line in a compaction
that drops more than one element in a row does not. Prefer `a[w-1]`: it says what
you mean, which is *the last thing I kept*.

**`w` never caught up with `r` after the first drop.** Once one element is
discarded, the gap is permanent and only widens. That gap is the reason no
temporary array appears anywhere.

## Why it is correct

The claim to prove is not "it removes duplicates". It is the general one, of
which dedup is an instance: the two-cursor sweep computes a **stable filter in
place**.

:::proof In-place compaction produces the kept subsequence, in order
**Setup.** Let `a⁰` denote the array's contents before the loop, `n` its length.
Let `keep(v, P)` be a predicate on the current element `v` and on `P`, the
sequence of elements kept so far. Consider

```
w = 0
for r in 0 .. n-1:
    if keep(a[r], a[0..w-1]):
        a[w] = a[r]
        w += 1
```

**Invariant.** At the top of the iteration with index `r`:

- **(I1)** `a[r .. n-1]` is identical to `a⁰[r .. n-1]`.
- **(I2)** `a[0 .. w-1]` is exactly the subsequence of `a⁰[0 .. r-1]` selected by
  `keep`, in its original relative order.
- **(I3)** `w <= r`.

**Base case.** Before the first iteration `r = 0` and `w = 0`. (I1) is the whole
array, unmodified. (I2) compares two empty sequences. (I3) is `0 <= 0`.

**Inductive step.** Assume (I1)–(I3) at `r < n`. The loop reads `a[r]`, which by
(I1) is `a⁰[r]` — the original element, not a copy of something else. It
evaluates `keep` on that value and on `a[0 .. w-1]`, which by (I2) is the true
list of kept elements. Two cases.

*Not kept.* Nothing is written. (I1) holds for `r+1` because `a[r+1 .. n-1]`
was untouched. (I2) holds because the kept subsequence of `a⁰[0 .. r]` equals
that of `a⁰[0 .. r-1]`. (I3) holds since `w <= r < r+1`.

*Kept.* We execute `a[w] = a⁰[r]`, then `w += 1`. By (I3) `w <= r`, so the
written index is at most `r`; therefore no index in `[r+1, n-1]` is touched and
(I1) holds for `r+1`. For (I2): the prefix `a[0 .. w-1]` was the kept
subsequence of `a⁰[0 .. r-1]`, and the write appends `a⁰[r]` at position `w`
without disturbing positions `0 .. w-1`, producing the kept subsequence of
`a⁰[0 .. r]` — appending at the end preserves relative order, which is what
*stable* means. The new `w` is `w+1 <= r+1`, so (I3) holds.

**Termination.** `r` takes each of the `n` values `0 .. n-1` exactly once; the
loop performs `n` iterations and stops.

**Conclusion.** On exit `r = n`, so by (I2) `a[0 .. w-1]` is exactly the
subsequence of `a⁰[0 .. n-1]` selected by `keep`, in order, and `w` is its
length. ∎
:::

Now say plainly what that argument leaned on, because each assumption is a bug
waiting for a careless line of code.

- **`w <= r` is load-bearing, and it is only true because a kept element advances
  both cursors by one.** If the transform can ever emit *more* elements than it
  consumes — inserting, duplicating, merging a second array in — the write cursor
  overtakes the read cursor and step "Kept" destroys data that (I1) promised was
  intact. This is not hypothetical: it is exactly why *Merge Sorted Array*, which
  writes `m + n` elements into an array holding `m` live ones, must be filled
  **from the back**. Reversed, the same proof works with the inequality flipped.
- **`keep` may only look at `a[r]` and at the kept prefix.** (I1) protects the
  tail and (I2) protects the prefix; nothing protects the arbitrary middle. A
  predicate that reads `a[r-2]` is reading memory the proof does not describe.
- **`keep` must be a function, not a coin flip.** It is evaluated once per
  element; if it is not deterministic, "the subsequence selected by `keep`" is not
  even well defined.
- **The array's length does not change.** The proof says nothing about
  `a[w .. n-1]`, so the caller must be told `w`. Returning the mutated array is a
  contract violation, not a style choice.
- **Stability is a consequence, not an extra.** Nothing in the argument sorts or
  reorders; elements are appended in the order encountered. If a problem wants
  the kept elements in a different order, this is the wrong loop.

## What it costs

**Time.** Count operations rather than asserting a symbol. The loop body runs
once per index, so there are exactly `n` reads of `a[r]` and `n` evaluations of
`keep`. Writes happen only on a keep, so there are `k <= n` of them, where `k` is
the size of the output. Total element operations: `2n + k <= 3n`, hence `Θ(n)`
time with a small constant, and — because `k` can be `0` — `Ω(n)` regardless of
the answer.

**Space.** Four scalars: `r`, `w`, `n`, and whatever `keep` carries. `O(1)`
extra, and that claim is honest only because the picture at the top is true; in a
language where "array" means a linked structure, none of this holds.

**The cost of doing it the obvious way.** Compare with deleting in place:

```
for i in reversed(range(n)):
    if not keep(a[i]):
        del a[i]
```

Each `del a[i]` shifts `n - i - 1` elements. If every element is dropped, the
total work is `(n-1) + (n-2) + … + 1 + 0 = n(n-1)/2`, which is `Θ(n²)`. At
`n = 10⁵` — the constraint line on *Array Leader Elements*, *Array Challenge (QR
Intern)* and most of this bank — that is about `5 × 10⁹` element moves against
`10⁵` for the sweep. The two programs are the same length and differ by five
orders of magnitude of work. This is the single highest-value trade in array
programming.

**The amortised cost of growth.** When you do build an output list, appending is
not free, but it is free *on average*, and the derivation matters. A dynamic
array with growth factor `g` reallocates whenever it fills: capacities go
`c₀, gc₀, g²c₀, …`. Reaching `n` elements means the final capacity `C` satisfies
`C <= g·n`, and a reallocation to capacity `c` copies the `c/g` elements already
there. The copies therefore total

```
C/g + C/g² + C/g³ + … = (C/g)·(1/(1 - 1/g)) = C/(g-1) <= g·n/(g-1)
```

For `g = 2` that is `2n` copies for `n` appends — two per element, amortised
`O(1)`. For `g = 1.5` it is `3n`. Grow by a *fixed* amount `c` instead and the
capacities are `c, 2c, 3c, …`, so the copies total
`c + 2c + … + n = Θ(n²/c)` — quadratic, whatever `c` is. Doubling is not a
micro-optimisation; it is the difference between linear and quadratic. The full
technique is [[amortized-analysis]].

**The costs people forget**, all of which turn a linear algorithm quadratic
without changing its shape:

- **Slicing copies.** `a[i:j]` in Python allocates and copies `j - i` elements. A
  "sliding window" that recomputes `sum(a[i:i+k])` each step is `Θ(nk)`, not
  `Θ(n)`. Carry a running sum instead ([[sliding-window]], [[prefix-sums]]).
- **`in` on a list is a scan.** `x in seen` is `Θ(len(seen))`. Inside a loop it is
  `Θ(n²)`. A set is the fix.
- **Front operations.** `insert(0, x)` and `pop(0)` are `Θ(n)` each.
- **Sorting is not free inside a loop.** One sort is `Θ(n log n)`; one per
  iteration is `Θ(n² log n)`.
- **Locality.** A sequential scan of contiguous memory is prefetched by the
  hardware; chasing pointers is not. Two `Θ(n)` algorithms with the same
  operation count can differ by a constant factor that is not small. This never
  changes a complexity class, and it regularly changes whether you pass.

## The implementation

```python run
def compact(a, keep):
    """Stable in-place filter. Returns k; a[:k] holds the kept elements."""
    w = 0
    for r in range(len(a)):
        if keep(a[r], a, w):
            a[w] = a[r]
            w += 1
    return w


def dedup_sorted(a):
    """Remove adjacent duplicates in place; returns the new length."""
    return compact(a, lambda v, arr, w: w == 0 or v != arr[w - 1])


def remove_value(a, x):
    return compact(a, lambda v, arr, w: v != x)


a = [1, 1, 2, 3, 3, 3, 5]
k = dedup_sorted(a)
print("dedup  ->", "length", k, "kept", a[:k], "garbage tail", a[k:])
assert k == 4 and a[:k] == [1, 2, 3, 5]

b = [4, 0, 4, 7, 4, 4]
m = remove_value(b, 4)
print("remove ->", "length", m, "kept", b[:m])
assert m == 2 and b[:m] == [0, 7]

empty = []
assert compact(empty, lambda v, arr, w: True) == 0
print("empty  -> length 0, no special case needed")

import random
rng = random.Random(3)
for _ in range(500):                      # against the obvious rebuilding version
    src = [rng.randrange(5) for _ in range(rng.randrange(0, 12))]
    want = sorted(set(src))
    arr = sorted(src)
    n = dedup_sorted(arr)
    assert arr[:n] == want, (src, arr, n)
    arr2 = list(src)
    n2 = remove_value(arr2, 2)
    assert arr2[:n2] == [v for v in src if v != 2], src
print("500 random arrays: compaction matches the list-comprehension reference")
```

Three lines are doing the work.

`a[w] = a[r]` is the whole algorithm. It is safe *only* because of invariant
(I3), and it is worth saying that to yourself every time you type it: "the write
index is behind the read index, so I am overwriting something I have already
consumed." When you cannot say that sentence, you need a second array or a
right-to-left pass.

`return w` — not `return a`, not `return a[:w]`. The length is the answer; the
slice is a convenience the caller may or may not want, and it costs a copy.

`w == 0 or v != arr[w - 1]` compares against the last **kept** element, not
against `arr[r - 1]`. For sorted dedup the two happen to coincide, as the trace
showed; for a filter that drops runs, only the first is correct. Writing the
correct one always costs nothing and removes a whole class of bug.

## Variants you will meet

**Two cursors from opposite ends.** Same memory, cursors converging instead of
trailing. *Squares of a Sorted Array* is the canonical one: squares are largest
at the two ends, so fill the output from the back while `lo` and `hi` walk
inward. Full treatment in [[two-pointers]].

**Writing from the back.** When the output is longer than what has been read,
reverse the direction so the write cursor trails again. *Merge Sorted Array*
(merge `b` into `a`, which has `n` spare slots at the end) is the archetype, and
the reason is exactly the failed assumption listed after the proof.

**Rotation by reversal.** Rotating right by `k` is three reversals and `O(1)`
space, no temporary array and no modular index chase. *Simple Array Rotation
Game*, *Minimum Right Shifts to Sort the Array* and *Cyclic Shift to Strictly
Descending Array* all live here.

**Prefix and difference arrays.** One pass converts an array into its running
sums, after which any range sum is a subtraction. The dual — add `d` at `l`,
subtract `d` at `r+1`, then take prefix sums — turns `q` range updates into
`O(n + q)`. *Minimum Number of Increments on Subarrays to Form a Target* is the
difference array read as a greedy. See [[prefix-sums]].

**Suffix scans.** Anything phrased "compared with everything to its right" is one
right-to-left pass carrying an aggregate. *Array Leader Elements* carries a
running maximum; the block below shows it. When the aggregate is "the nearest
larger element" rather than "the largest", you need [[monotonic-stack]].

**The array as its own hash table.** When the values are a permutation of
`1 .. n`, index `v-1` *is* the slot for value `v`, so membership needs no extra
memory. *First Missing Number in a Consecutive Array* is this. See [[cyclic-sort]].

**Encoding two values in one slot.** If values are bounded by `m`, store
`old + m·new` and recover both with `%` and `//`. *Construct New Array* and
*Meandering Array* — interleave the front and the back — can be done this way in
`O(1)` space. See [[in-place-rearrangement]].

**Rank and coordinate compression.** Sort the distinct values, map each to its
position, rewrite the array in original order. *Array Rank Transform* and *Rank
Transform an Array* are the bare exercise; as a subroutine it makes values usable
as indices. See [[sorting]] and [[custom-comparators]].

**Two dimensions on one dimension.** A matrix is an array with `index = r·cols +
c`. The row-major order is why scanning a matrix row by row is faster than column
by column. See [[matrix-traversal]].

```python run
def rotate_right(a, k):
    """Rotate a right by k in place, using three reversals and no buffer."""
    n = len(a)
    if n == 0:
        return a
    k %= n

    def rev(i, j):                       # reverse a[i..j] inclusive
        while i < j:
            a[i], a[j] = a[j], a[i]
            i += 1
            j -= 1

    rev(0, n - 1)                        # (A B) -> rev(B) rev(A)
    rev(0, k - 1)                        #       -> B rev(A)
    rev(k, n - 1)                        #       -> B A
    return a


def leaders(nums):
    """Elements strictly greater than every element to their right, in order."""
    out, best = [], None
    for i in range(len(nums) - 1, -1, -1):
        if best is None or nums[i] > best:
            out.append(nums[i])
            best = nums[i] if best is None else max(best, nums[i])
    out.reverse()
    return out


a = [1, 2, 3, 4, 5, 6, 7]
print("rotate right by 3:", rotate_right(list(a), 3))
assert rotate_right(list(a), 3) == [5, 6, 7, 1, 2, 3, 4]
assert rotate_right(list(a), 0) == a and rotate_right(list(a), 7) == a
assert rotate_right(list(a), 10) == rotate_right(list(a), 3)
print("k = 0, k = n and k = n + 3 all agree with the slice form")

import random
rng = random.Random(5)
for _ in range(500):
    n = rng.randrange(0, 9)
    src = [rng.randrange(20) for _ in range(n)]
    k = rng.randrange(0, 15)
    want = src if n == 0 else src[-(k % n):] + src[:-(k % n)] if k % n else list(src)
    assert rotate_right(list(src), k) == want, (src, k)
print("500 random rotations match the slicing reference")

nums = [16, 17, 4, 3, 5, 2]
print("leaders of", nums, "->", leaders(nums))
assert leaders(nums) == [17, 5, 2]
assert leaders([5, 5, 5]) == [5] and leaders([]) == []
print("equal values: only the rightmost survives, as the statement requires")
```

`rev(0, n-1)` then `rev(0, k-1)` then `rev(k, n-1)` deserves the one-line reason.
Write the array as `A·B` with `|B| = k`. Reversing the whole thing gives
`rev(B)·rev(A)`, because reversing a concatenation reverses the pieces and swaps
them. Reversing the first `k` slots turns `rev(B)` back into `B`; reversing the
last `n-k` turns `rev(A)` back into `A`. Result: `B·A`, which is the right
rotation by `k`. Each element is touched at most twice, so it is `Θ(n)` with two
scalars of state.

`k %= n` is not defensive programming, it is the specification: rotating by `n`
is the identity, and the tests will contain `k > n`.

## Recognising it in a statement

Ordered by how much the phrase should move you.

1. **"in place", "O(1) extra space", "return the new length", "modify nums
   directly"** — the two-cursor compaction, essentially always. *Remove
   Duplicates From Sorted Array In Place*, *Deduplicate a Sorted Array In Place*.
2. **"contiguous", "subarray", "window", "consecutive elements"** — a sweep with
   running state: [[sliding-window]] or [[prefix-sums]]. *Count Descending
   Subarrays*, *Count Strictly Increasing Contiguous Windows*.
3. **"return the result in the original order"** attached to something that
   obviously wants sorting — you must carry indices, or sort a copy and map back.
   *Array Rank Transform* says it outright.
4. **"every element to its left" / "to its right"** — a prefix pass, a suffix
   pass, or both, combined at each index. *Array Leader Elements* is the suffix
   form; *Array Challenge (QR Intern)*, which asks for a signed sum against all
   elements to the left, is the prefix form and is `Θ(n²)` if taken literally at
   `n = 10⁵` — the intended solution is a running count and a running sum.
5. **`1 <= n <= 10^5` with an obvious nested loop.** `10¹⁰` operations is not a
   plan. One or two passes is, and [[complexity-analysis]] says which.
6. **The values are a permutation of `1 .. n`, or bounded by a small constant.**
   Indices become storage. *First Missing Number in a Consecutive Array*.
7. **Two arrays, and pairs across them.** *Count Cross-Array Target-Sum Pairs*:
   the double loop is `4 × 10¹⁰` at the stated limits, and counting one side into
   a dictionary makes it linear.

The anti-signals:

- **"subsequence"** — not contiguous, exponentially many, so no cursor helps.
- **Insertions and deletions in the middle, interleaved with reads.** The array
  is the wrong container.
- **"any order" plus "distinct values"** — position is not meaningful, so you are
  really being handed a set, and sorting or hashing is the move.
- **Repeated "the smallest remaining" or "the k-th largest so far"** — [[heap]]
  or [[quickselect]], not a re-scan.

## Traps

**Mutating a list while iterating it.** The iterator holds an index; removing an
element shifts the tail left under it and one element is skipped. The symptom is
brutal: the code works on inputs with no adjacent matches and silently fails when
two matches are neighbours. Demonstrated below.

**Aliasing.** `b = a` binds a second name to the same array; `b = a[:]` copies.
Worse, `[[0] * m] * n` builds `n` references to **one** row, so writing
`grid[0][0]` writes every row. Symptom: a matrix where whole columns change at
once. Demonstrated below.

**Returning the array instead of the length.** After compaction the tail is
garbage. Symptom: extra trailing elements that happen to look plausible, so the
first test passes.

**Negative indices do not raise.** `a[i - 1]` with `i = 0` returns the last
element in Python instead of failing. Symptom: an answer that is wrong only when
the correct answer involves the first element. Guard the index, do not rely on an
exception that will not come.

**Comparing against an overwritten slot.** In a compaction, `a[r-2]` is scratch.
Symptom: correct on inputs where nothing was dropped yet, wrong afterwards.

**Off-by-one in the half-open habit.** Pick `a[i:j]` meaning `i` inclusive, `j`
exclusive, and never mix. The length is `j - i`, the last index is `j - 1`, and
an empty range is `i == j`. Most index bugs are a silent switch between
conventions mid-function.

**Integer width, in languages that have it.** *Average of a Fixed-Size Array*
specifies that the sum fits in a signed 64-bit integer, and *Count Cross-Array
Target-Sum Pairs* specifies 64-bit arithmetic throughout. Those sentences are
there because summing `10⁵` values of magnitude `10⁹` exceeds 32 bits. Python
will not warn you; the interviewer asking you to port it to Java will.

**The empty array.** `max(a)` raises, `a[0]` raises, and the mean is undefined.
Every sweep in this chapter handles `n = 0` by doing nothing, which is why it was
worth asserting.

```python run
nums = [3, 4, 4, 5]

def wrong_remove(a, x):
    a = list(a)
    for v in a:                 # iterating the list being mutated
        if v == x:
            a.remove(v)
    return a

def right_remove(a, x):
    a = list(a)
    w = 0
    for r in range(len(a)):
        if a[r] != x:
            a[w] = a[r]
            w += 1
    return a[:w]

print("input             ", nums)
print("mutate-while-iter ", wrong_remove(nums, 4), "<- one 4 survives")
print("two cursors       ", right_remove(nums, 4))
assert wrong_remove(nums, 4) == [3, 4, 5]
assert right_remove(nums, 4) == [3, 5]

shared = [[0] * 3] * 3          # three references to ONE row
proper = [[0] * 3 for _ in range(3)]
shared[0][0] = 9
proper[0][0] = 9
print("[[0]*3]*3 after one write:", shared, "<- every row changed")
print("comprehension            :", proper)
assert shared == [[9, 0, 0]] * 3 and proper[1] == [0, 0, 0]
assert shared[1] is shared[0] and proper[1] is not proper[0]
print("the two rows are the same object:", shared[1] is shared[0])
```

The first failure is worth understanding rather than memorising. At index 1 the
iterator yields `4`, `remove` deletes it, and the second `4` slides from index 2
to index 1 — but the iterator has already moved on to index 2, which now holds
`5`. Exactly the elements that follow a removal are skipped, which is why a
single stray duplicate survives. The compaction cannot have this bug, because its
read cursor advances over memory that the proof guarantees is untouched.

## What to memorise

Very little. One template, one sentence, one habit.

**The template**, which should arrive without thought:

```python
w = 0
for r in range(len(a)):
    if keep(a[r]):
        a[w] = a[r]
        w += 1
return w              # a[:w] is the answer; the tail is garbage
```

**The sentence** that turns a problem into it: *"Can I produce the answer by
reading left to right and writing no faster than I read?"* If yes, the extra
space is `O(1)` and the code is five lines. If the answer needs to write faster
than it reads, run the same loop from the right.

**The habit**: before writing `a[w] = a[r]`, say what is true of `a[0..w-1]` and
of `a[r..n-1]`. Two claims, out loud. Almost every array bug is one of those two
claims being false at the moment of the write — the tail already clobbered, or
the prefix not actually holding what you think it holds.

Numbers worth carrying. `1 + 2 + … + n = n(n+1)/2`, which is what any
shift-in-a-loop costs. Doubling a dynamic array costs `2n` copies for `n`
appends; growing by a constant costs `Θ(n²)`. `n = 10⁵` means `n² = 10¹⁰`, which
is out of reach, while `n log₂ n ≈ 1.7 × 10⁶`, which is nothing. A range `[i, j)`
has length `j - i`. And `k % n` before any rotation.

## Check yourself

:::check
Why does in-place compaction need no temporary buffer, when the "obvious"
implementation builds a new list of the kept elements?
--
Because the elements it has already read and decided to drop are dead memory, and
they sit exactly where the output needs to go. Formally, invariant (I3) says
`w <= r`: the write index never passes the read index, so every write lands on a
slot whose original value has already been consumed — either copied forward or
deliberately discarded.

The buffer is not absent; it is the gap between `w` and `r`, and that gap grows
by one for each element dropped, which is precisely the amount of room the output
needs to *not* need. This is also the reason the technique fails the moment the
transform can emit more elements than it consumes: then `w` would overtake `r`
and the writes would land on unread data.
:::

:::check
*Merge Sorted Array* gives you `a` with `m` values followed by `n` empty slots,
and `b` with `n` values, both sorted, and asks you to merge into `a`. Why does
the natural left-to-right merge fail, and what exactly fixes it?
--
Left to right, the write cursor starts at index 0 and the read cursor into `a`
also starts at index 0. The first time an element of `b` is smaller, you write it
to `a[0]` and destroy `a[0]` before reading it. The write cursor is now ahead of
`a`'s read cursor — the `w <= r` assumption is broken, and the proof's (I1) no
longer holds.

The fix is to fill from the back: set `w = m + n - 1`, `i = m - 1`, `j = n - 1`,
and write the larger of `a[i]`, `b[j]` at `w`, stepping all three downward. Now
the claim is `w >= i` at all times, which holds because `w - i = (remaining in b)
>= 0` and shrinks only when an element of `b` is consumed. The empty tail of `a`
gives the write cursor its head start, so it can never catch `i`. Same proof,
same five lines, mirrored.
:::

:::check
A candidate says: "Removing all the `4`s from a list of `n` elements with a loop
of `list.remove(4)` is `O(k)` where `k` is the number of 4s — each call is one
operation." Where are they wrong?
--
Two errors, and the second is the expensive one.

First, `remove` is not one operation. It scans for the value (`Θ(n)` in the worst
case) and then shifts every following element one slot left (`Θ(n)` again),
because the array is contiguous and may not have gaps. Removing `k` elements is
`Θ(kn)`, which at `n = 10⁵` with half the array matching is around `5 × 10⁹`
element moves.

Second — and this is a correctness bug, not a performance one — if the loop
iterates over the same list it mutates, elements are skipped. After a removal at
index `i`, the element that slides into index `i` is never examined, because the
iterator has already advanced to `i + 1`. The runnable trap block above shows a
`4` surviving for exactly this reason.

The correct statement: it is `Θ(n)` with the two-cursor sweep, and the sweep is
also the version that cannot skip anything.
:::

:::check
Rotating an array right by `k` is done with three reversals. Why does
`reverse(whole)`, then `reverse(first k)`, then `reverse(rest)` produce the
rotation — and why is `k %= n` not optional?
--
Write the array as the concatenation `A·B`, where `B` is the last `k` elements.
The right rotation by `k` is `B·A`.

Reversal distributes over concatenation with a swap: `reverse(A·B) =
reverse(B)·reverse(A)`. So after the first step the array is
`reverse(B)·reverse(A)`, with `reverse(B)` occupying exactly the first `k` slots
because `|B| = k`. Reversing those `k` slots restores `B`; reversing the
remaining `n - k` restores `A`. The array is now `B·A`.

`k %= n` is needed because the argument defines `B` as *the last `k` elements*,
which is meaningless for `k >= n`. Rotating by `n` is the identity, so only
`k mod n` carries information — and with `k > n` the second `rev(0, k-1)` would
index past the end or silently do the wrong thing. It is part of the derivation,
not a guard bolted on afterwards.
:::

:::check
In the dedup trace, step 3 overwrote `a[2]`, destroying an original value. Yet
the loop is allowed to compare `a[r]` with `a[r-1]`. Explain the discrepancy
precisely, and say which comparison you should actually write.
--
Index `j` is written only during the iteration where `w == j`. Since `w <= r`
always, that iteration has `r >= j`. So for index `r-1` to be written *before*
the loop reaches step `r`, it would have to happen at step `r-1` with `w = r-1` —
and then the statement executed is `a[r-1] = a[r-1]`, which changes nothing.
Conclusion: at the top of step `r`, `a[r-1]` still holds its original value.
Exactly one slot of grace; `a[r-2]` genuinely can be, and in the trace was,
clobbered.

You should still write `a[w-1]`. It survives any compaction, not just one that
drops single elements, and it expresses the actual rule — "different from the
last element I kept" — rather than relying on a one-slot accident of the write
schedule. Correct code that is correct for a reason you have to re-derive is a
liability under time pressure.
:::

:::check
`grid = [[0] * 3] * 3` and `grid = [[0] * 3 for _ in range(3)]` print identically.
Why do they behave differently, and what general rule about arrays does the
difference illustrate?
--
`[x] * n` builds an array of `n` **references to the same object** `x`. With
`x = [0, 0, 0]`, all three rows are one list, so `grid[0][0] = 9` is visible
through `grid[1]` and `grid[2]`. The comprehension evaluates `[0] * 3` afresh on
each iteration and produces three distinct lists.

The general rule: an array stores fixed-width slots, and for anything larger than
a machine word the slot holds a reference, not the object. Copying an array
therefore copies references — a *shallow* copy. `b = a[:]`, `list(a)` and
`a.copy()` all protect you from someone reassigning `a[i]`; none of them protects
you from someone mutating `a[i]` itself. That is the same fact behind `b = a`
aliasing the whole array, and behind passing an array to a function that modifies
it in place.
:::
