# Two Pointers

> Two pointers is not "use two indices". It is the discovery that looking at one
> pair of positions can disqualify an entire row or column of the pairs you would
> otherwise have to try, which turns a quadratic search into a single sweep.

## When you reach for it

You reach for two pointers when the object you are searching for is a **pair of
positions** — a left end and a right end, a slot to read from and a slot to write
to, a place in list A and a place in list B — and when a single comparison at one
pair tells you something about many *other* pairs.

That second half is the whole trigger, and it is the half people forget. There
are `n(n-1)/2` pairs in an array. If probing one pair only rules out that pair,
you have written a nested loop with extra vocabulary. If probing one pair rules
out a whole column of pairs — "no partner of `a[lo]` can ever work" — then a few
hundred thousand probes become a few hundred thousand, not a few billion.

The usual source of that leverage is **order**. In a sorted array,
`a[lo] + a[hi]` being too small tells you `a[lo]` paired with *anything* still in
range is too small, because everything still in range is at most `a[hi]`. Sorted
inputs, palindromic ends, already-merged streams, monotone heights: all of them
give you a comparison whose verdict generalises. But order is the *source*, not
the requirement — exactly as sortedness is the source and not the requirement for
[[binary-search]].

This bank has 192 problems that use the technique, ranking it #22 of 150 topics,
and they sort cleanly into three families. Once you have names for them you will
stop seeing "a two pointer problem" and start seeing which one:

- **Converging** — the pointers start at opposite ends and walk toward each
  other. *Container With Most Water*, *3Sum*, *Trapping Rain Water*, *Valid
  Palindrome II*, *Find Pair Closest to K (for E5 :)*.
- **Same direction** — a fast reader and a slow writer, or a lagging index that
  marks the start of a run. *Remove Duplicates From Sorted Array In Place*,
  *Sort Colors*, *Run-Length String Compression*, *Longest Contiguous Character
  Run*.
- **Two sequences** — one pointer per input, advancing whichever is behind.
  *Merge Sorted Array*, *Interval List Intersections*, *Squares of a Sorted
  Array*, *Find the Intersection Node of Two Linked Lists*.

And the shape that makes it the *wrong* tool. If the comparison at `(i, j)`
says nothing about `(i, j-1)` — an unsorted array where you need an exact pair
sum — you want [[hash-tables]], which buys generalisation with memory instead of
order. If you must return the *original* indices and the array is unsorted,
sorting destroys the answer unless you carry the indices along. And if the region
between the pointers is scored by a predicate that can turn from good to bad and
back as the window grows, you are not converging on anything: that is
[[sliding-window]], a different animal wearing the same two variables.

## The idea

Lay out every candidate pair as a grid. Column `i`, row `j`, one cell per pair
with `i < j`: a triangle of about `n²/2` cells. A brute-force double loop visits
every cell. Two pointers walks a single staircase from one corner, and each step
of the staircase **erases an entire row or an entire column** — not because you
checked those cells, but because one comparison proved none of them can be the
answer.

<svg viewBox="0 0 640 300" role="img" aria-label="grid of index pairs with a staircase path, each step deleting a full row or column">
  <g>
    <line x1="90" y1="40" x2="90" y2="244"/>
    <line x1="124" y1="40" x2="124" y2="244"/>
    <line x1="158" y1="40" x2="158" y2="244"/>
    <line x1="192" y1="40" x2="192" y2="244"/>
    <line x1="226" y1="40" x2="226" y2="244"/>
    <line x1="260" y1="40" x2="260" y2="244"/>
    <line x1="294" y1="40" x2="294" y2="244"/>
    <line x1="90" y1="40" x2="294" y2="40"/>
    <line x1="90" y1="74" x2="294" y2="74"/>
    <line x1="90" y1="108" x2="294" y2="108"/>
    <line x1="90" y1="142" x2="294" y2="142"/>
    <line x1="90" y1="176" x2="294" y2="176"/>
    <line x1="90" y1="210" x2="294" y2="210"/>
    <line x1="90" y1="244" x2="294" y2="244"/>
    <rect class="fill" x="90" y="40" width="34" height="34"/>
    <rect class="fill" x="90" y="74" width="34" height="34"/>
    <rect class="fill" x="124" y="74" width="34" height="34"/>
    <rect class="fill" x="124" y="108" width="34" height="34"/>
    <rect class="fill" x="158" y="108" width="34" height="34"/>
    <line x1="90" y1="244" x2="294" y2="40"/>
    <text x="196" y="200">i = j</text>
    <text x="150" y="268">i (lo) increases</text>
    <text x="20" y="45">j (hi)</text>
    <text x="20" y="70">falls</text>
    <text x="330" y="60">one probe per staircase step</text>
    <text x="330" y="92">sum too small: delete column i</text>
    <text x="330" y="124">sum too big: delete row j</text>
    <text x="330" y="156">5 probes here, not 15 pairs</text>
    <text x="330" y="188">n probes in general, not n squared</text>
  </g>
</svg>

The staircase never backtracks. `lo` only rises, `hi` only falls, so the number
of steps is bounded by how far they can travel — at most `n` between them. That
one sentence is the entire cost analysis, and it is why all three families are
linear even though they look like nested loops.

The three families differ only in where the pointers start and what the rule for
moving is:

```python
# converging                    # same direction               # two sequences
lo, hi = 0, len(a) - 1          w = 0                          i = j = 0
while lo < hi:                  for r in range(len(a)):        while i < len(a) and j < len(b):
    if too_small(lo, hi):           if keep(a[r]):                 if a[i] <= b[j]:
        lo += 1                         a[w] = a[r]                    take(a[i]); i += 1
    else:                               w += 1                     else:
        hi -= 1                                                        take(b[j]); j += 1
```

Three shapes, one principle: two indices, each moving in one direction only, and
a rule that decides which one moves. Get the rule right and you are done; get it
wrong and the loop still runs in linear time and still returns an answer, just
not the right one.

## Worked by hand

Sorted array `a = [1, 3, 4, 6, 8, 11]`, target `10`. Fifteen pairs exist. Watch
how few we look at.

Start `lo = 0`, `hi = 5`.

| step | lo | hi | `a[lo]` | `a[hi]` | sum | vs 10 | move | what dies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 5 | 1 | 11 | 12 | too big | `hi = 4` | every pair containing 11 |
| 2 | 0 | 4 | 1 | 8 | 9 | too small | `lo = 1` | every pair containing 1 |
| 3 | 1 | 4 | 3 | 8 | 11 | too big | `hi = 3` | every pair containing 8 |
| 4 | 1 | 3 | 3 | 6 | 9 | too small | `lo = 2` | every pair containing 3 |
| 5 | 2 | 3 | 4 | 6 | 10 | equal | return `(2, 3)` | — |

Five probes, fifteen pairs. Three things in that table are worth more than the
answer.

**The "what dies" column is the algorithm.** At step 1 the sum was too big, and
the *smallest* available partner for 11 was `a[0] = 1`. If 11 cannot make the
target with the smallest thing left, it cannot make it with anything left
either — so the entire row `j = 5` is gone, five pairs at one stroke. At step 2
the sum was too small, and the *largest* available partner for 1 was `a[4] = 8`;
same argument mirrored, and column `i = 0` is gone. Each step removes a full row
or column, and there are only `2n` of those, which is the counting argument
hiding behind the linear running time.

**The pointers never take back a move.** Nothing in the trace ever decrements
`lo`. If your intended logic needs `lo` to go back and re-examine something, the
elimination you thought you had is not real, and the technique does not apply —
no amount of careful coding will rescue it.

**The loop condition is `lo < hi`, not `lo <= hi`.** At step 5 we happened to
return. Had the target been 8, the pointers would have met at `lo = hi = 2` and
the loop would stop, because a pair needs two distinct slots. With `<=` the code
would happily report `4 + 4 = 8` using one element twice. That single character
is the most common bug in this whole topic and there is a demonstration of it in
*Traps*.

## Why it is correct

The trace makes the algorithm look obvious, which is exactly when a proof is
worth writing: "obvious" is where the duplicate-handling and empty-range bugs
live. Here is the argument for the converging form, stated so that the counting
and closest-pair variants inherit it.

:::proof Correctness of the converging sweep
**Setup.** Let `a[0..n-1]` be sorted non-decreasing and let `t` be the target.
Call a pair `(i, j)` **good** when `0 <= i < j <= n-1` and `a[i] + a[j] == t`.
Write `S(lo, hi)` for the set of pairs `(i, j)` with `lo <= i < j <= hi` — the
cells of the grid still inside the current window.

**Invariant.** At the top of every iteration: *every* good pair of the array lies
in `S(lo, hi)`, and `lo <= hi`.

**Base case.** Before the first iteration `lo = 0` and `hi = n-1`, so `S(lo, hi)`
is the set of all pairs with `i < j`. Every good pair is one of those. If
`n = 0` or `n = 1` the loop body never runs and there are no good pairs to
account for.

**Inductive step.** Assume the invariant and `lo < hi`. Let `s = a[lo] + a[hi]`.

- `s == t`. The algorithm returns `(lo, hi)`, which is good by definition, and
  `lo < hi` so it is a legal pair. Nothing to preserve.
- `s < t`. Take any `j` with `lo < j <= hi`. Sortedness gives `a[j] <= a[hi]`,
  hence `a[lo] + a[j] <= a[lo] + a[hi] = s < t`, so `(lo, j)` is not good. That
  is *every* pair in `S(lo, hi)` whose first index is `lo`. Removing them leaves
  `S(lo+1, hi)`, which therefore still contains every good pair of the array.
  Setting `lo := lo + 1` restores the invariant.
- `s > t`. Symmetrically, for any `i` with `lo <= i < hi`, sortedness gives
  `a[i] >= a[lo]`, so `a[i] + a[hi] >= s > t` and `(i, hi)` is not good. Every
  pair with second index `hi` is eliminated, `S(lo, hi-1)` retains every good
  pair, and `hi := hi - 1` restores the invariant.

In both surviving branches `lo <= hi` still holds, because we only moved a
pointer when `lo < hi`.

**Termination.** Let `Φ = hi - lo`, a non-negative integer. Every iteration that
does not return decreases `Φ` by exactly 1. A non-negative integer cannot
decrease forever, so after at most `n - 1` iterations the loop reaches `Φ = 0`
and the condition `lo < hi` fails.

**Conclusion.** If the loop returns, it returns a good pair. If the loop exits,
then `lo == hi`, so `S(lo, hi)` is empty — there is no pair `i < j` inside a
single index. The invariant says every good pair of the array lies in that empty
set, so the array has no good pair, and reporting "none" is correct. ∎
:::

Now the part that matters more than the proof: **what did it use?**

1. **Sortedness, twice.** Once for `a[j] <= a[hi]` and once for
   `a[i] >= a[lo]`. Feed the loop an unsorted array and both eliminations become
   false claims. The code still runs in linear time and still returns something.
2. **Monotone combination.** The step `a[lo] + a[j] <= a[lo] + a[hi]` needs the
   combining operation to be non-decreasing in each argument. Addition is.
   Multiplication with negative numbers is not. Neither is XOR, nor string
   concatenation compared lexicographically. Swap `+` for one of those and the
   proof collapses even on sorted input.
3. **`i < j`, strictly.** The grid is a triangle, not a square. The proof spoke
   of pairs with two distinct indices throughout, which is what `while lo < hi`
   enforces.
4. **Whole rows and whole columns.** Each move discarded *every* surviving pair
   containing one element. A rule that eliminates only some of a column — "skip
   this one, it looks unpromising" — breaks the invariant immediately, and the
   failure shows up only on inputs you did not test.
5. **Existence, not enumeration, unless you are careful.** The invariant is
   strong enough that counting variants work too: nothing good is ever thrown
   away. But the `s == t` branch is where enumeration needs extra thought,
   because after recording a match you must advance *past* it on both sides or
   you will report it again.

:::note The same argument, with a different elimination rule
*Container With Most Water* is not about sums, but the shape of the proof is
identical. The area of the pair `(lo, hi)` is `(hi - lo) * min(h[lo], h[hi])`.
Suppose `h[lo] < h[hi]` and take any `j < hi` with `j > lo`. Then
`area(lo, j) = (j - lo) * min(h[lo], h[j]) <= (j - lo) * h[lo] < (hi - lo) * h[lo] = area(lo, hi)`.
So every remaining pair in column `lo` is strictly worse than the pair we just
measured — the column dies, and retiring `lo` loses nothing. Different problem,
same sentence: *one probe proves a whole column is dominated*.
:::

:::note Why filling from the lower side is safe in Trapping Rain Water
The water above index `i` is `min(maxLeft(i), maxRight(i)) - h[i]`, which looks
like it needs both maxima. The sweep maintains the invariant
`lmax <= max(h[hi..n-1])` and `rmax <= max(h[0..lo])`: whatever the left has seen
is matched by a bar still standing on the right, and vice versa. Initially both
maxima are 0, so it holds. When `h[lo] < h[hi]` we set `lmax := max(lmax, h[lo])`,
which is still at most `max(h[hi..n-1])` because `h[lo] < h[hi]`. That inequality
is exactly the statement that the left maximum is the binding constraint at index
`lo`, so `lmax - h[lo]` is the true water there, no lookahead required.
:::

## What it costs

**Converging.** Use the potential `Φ = hi - lo`. It starts at `n - 1`, is a
non-negative integer, and every iteration decreases it by exactly 1. So the loop
body runs at most `n - 1` times, each time doing O(1) work: **Θ(n) time, O(1)
extra space.** Compare with the double loop, which touches `n(n-1)/2` pairs. At
`n = 2·10⁵` — the constraint you will see on these problems — that is
`2·10¹⁰` pair visits against `2·10⁵` probes, a factor of a hundred thousand.
This is not a constant-factor improvement, which is why the technique is worth a
chapter.

**Same direction, with an inner loop.** Here the counting is less obvious and
more instructive. A compaction or run-detection loop often looks like this:

```python
for r in range(n):
    while w < r and not ok(w, r):
        w += 1
```

The nesting suggests `O(n²)`. It is `O(n)`. The reason is a summation, not a
bound per iteration: `w` starts at 0, never decreases, and never exceeds `n`, so
the total number of executions of the inner body across the whole outer loop is
at most `n`. The work is `Σ (advances of r) + Σ (advances of w) <= 2n`. This is
the standard **amortized** argument — you may not bound one iteration, but you
can bound the sum, because each pointer's movement is paid for once and never
refunded. Every [[sliding-window]] analysis is this same sentence.

**Two sequences.** Each iteration consumes one element from `a` or one from `b`
and never un-consumes it, so the loop runs at most `len(a) + len(b)` times:
**Θ(n + m)**. The tail flush is `O(n + m)` too, and forgetting it is a
correctness bug, not a performance one.

**The costs people forget.**

- *The sort.* If the input is not already sorted, `two_sum` on a sorted array is
  `Θ(n log n)` end to end, and the elegant linear sweep is the cheap part. That
  is also why the hash-table solution — `Θ(n)` time, `Θ(n)` space, no sort — is
  the better answer when the array is unsorted and you need original indices.
- *3Sum.* The outer index runs `n - 2` times and each inner sweep costs at most
  `n - i - 1` probes, so the total is `Σᵢ (n - i - 1) = Θ(n²)`. The `Θ(n log n)`
  sort disappears into that. The extra space is `O(1)` beyond the output, and the
  output itself can hold `Θ(n²)` triplets, which is the real memory risk.
- *The comparison.* In *Valid Palindrome After Normalization* each step skips
  non-alphanumeric characters before comparing. Those skips are pointer moves
  like any other, so the total stays linear — but only because a skipped
  character is never revisited. If your per-step work is itself a scan, the
  product is back.
- *Building the output.* In Python, `out += s[i]` inside the loop is `O(n²)`
  because strings are immutable and each concatenation copies. Append to a list
  and `"".join` at the end. The sweep is linear; the bookkeeping does not have to
  ruin it.

## The implementation

One block, all three families, each checked against brute force on random input
so the claims are not decoration.

```python run
import random


def two_sum_sorted(a, target):
    """Indices lo < hi with a[lo] + a[hi] == target, or None. a must be sorted."""
    lo, hi = 0, len(a) - 1
    while lo < hi:                      # strict: a pair needs two distinct slots
        s = a[lo] + a[hi]
        if s == target:
            return (lo, hi)
        if s < target:
            lo += 1                     # a[lo] fails even with the largest partner
        else:
            hi -= 1                     # a[hi] fails even with the smallest partner
    return None


def dedup_sorted(a):
    """Compact a sorted list in place; return the length of the kept prefix."""
    if not a:
        return 0
    w = 1                               # w = how many kept so far = next free slot
    for r in range(1, len(a)):
        if a[r] != a[w - 1]:            # compare against the last KEPT value
            a[w] = a[r]
            w += 1
    return w


def merge(a, b):
    """Merge two sorted lists into one sorted list."""
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    out.extend(a[i:]); out.extend(b[j:])     # exactly one tail is non-empty
    return out


a = [1, 3, 4, 6, 8, 11]
print("sorted two-sum on", a)
print("  target 10 ->", two_sum_sorted(a, 10), " target 19 ->", two_sum_sorted(a, 19))
print("  target 13 ->", two_sum_sorted(a, 13), "(no pair)")
d = [0, 0, 1, 1, 1, 2, 3, 3]
k = dedup_sorted(d)
print("dedup        ", d[:k], "kept", k, "of 8; tail left as junk:", d[k:])
print("merge        ", merge([1, 4, 4, 9], [2, 4, 10]))

rng = random.Random(7)
for _ in range(400):
    n = rng.randrange(0, 9)
    xs = sorted(rng.randrange(-8, 9) for _ in range(n))
    t = rng.randrange(-16, 17)
    brute = any(xs[i] + xs[j] == t for i in range(n) for j in range(i + 1, n))
    got = two_sum_sorted(xs, t)
    assert (got is not None) == brute, (xs, t, got)
    assert got is None or (got[0] < got[1] and xs[got[0]] + xs[got[1]] == t)
    ys = sorted(rng.randrange(0, 5) for _ in range(n))
    copy = list(ys)
    assert copy[:dedup_sorted(copy)] == sorted(set(ys))
    zs = sorted(rng.randrange(0, 20) for _ in range(rng.randrange(0, 6)))
    assert merge(ys, zs) == sorted(ys + zs)
print("400 random cases agree with brute force on all three skeletons")
```

Three lines are doing the real work.

`while lo < hi` is the pair-validity condition, not a loop-bounds detail. Read it
as "there are still at least two distinct slots in the window". It is also the
termination guarantee, since `hi - lo` drops by one per iteration.

`if a[r] != a[w - 1]` compares the reader against the **last value kept**, not
against `a[r - 1]`. Those coincide here because the input is sorted and we keep
the first of each run, but the `w - 1` form is the one that survives when the
filter gets more interesting — *Keep At Most Two Copies in a Sorted Array* is
literally this line with `a[w - 2]`. Think of `w` as a fact: "`a[0..w-1]` is the
finished answer". Every write must keep that fact true.

`out.extend(a[i:]); out.extend(b[j:])` is the flush. Exactly one of the two
slices is non-empty, and writing both unconditionally is shorter and safer than
an `if`. Forgetting this line is the classic merge bug, and it only shows up when
one input runs out early — which random tests catch and hand-picked examples
often do not.

## Variants you will meet

**Converging on a target.** Two-sum on sorted data, and its relatives: *Find Pair
Closest to K (for E5 :)* keeps the best difference seen instead of returning on
equality; *Unique Pairs With Target Sum* counts distinct pairs and so must skip
past duplicate values on both sides after a hit.

**Fix one, sweep two.** *3Sum*, *4Sum*, *Three Sum Closest*, *Increasing-Value
Triplets Under a Threshold*: sort, pin the outer index or indices, and run the
converging sweep on the remainder. `k`-sum costs `Θ(n^(k-1))` this way.

**Dominance elimination.** *Container With Most Water* and *Trapping Rain Water*
move the pointer at the weaker side because the weaker side can never improve.
The rule is not "the smaller value" as a ritual — it is whichever side you can
prove is dominated.

**Read-and-write compaction.** *Remove Duplicates From Sorted Array In Place*,
*Keep at Most K Occurrences in a Sorted Array*, *Filter Odds and Reverse Evens*.
One pointer reads, one writes, and `w <= r` always, so you never overwrite
something you have not read yet. See [[in-place-rearrangement]].

**Three-way partition.** *Sort Colors* is the Dutch national flag: `low`, `mid`,
`high`, with `mid` scanning and the other two marking region boundaries. Three
pointers, same discipline — each moves one way, and the regions they delimit are
the invariant.

**Merge of two sequences.** *Merge Sorted Array* (in place, filling from the back
so you never clobber unread data), *Interval List Intersections* and *Intersect
Two Sorted Interval Lists* (advance whichever interval ends first), *Set
Intersection*. See [[merge-sort]], [[k-way-merge]] and [[intervals]].

**Subsequence matching.** *Check a Repeated String as a Subsequence* and
*Validate a Word Abbreviation*: one pointer per string, advance the pattern
pointer only on a match, and the greedy earliest match is optimal.

**From both ends inward, symmetrically.** *Valid Palindrome II*, *Minimum
Deletions for a Non-Palindrome*, *Alternate String Ends*. See [[palindromes]].

**Same array, different speeds.** When the two pointers move at different rates
along one structure — cycle detection, the middle node, the `k`-th from the end —
you are in [[fast-slow-pointers]]. *Find the Intersection Node of Two Linked
Lists* and *Middle Node Of A Linked List* live there.

**Variable window.** When the right pointer expands and the left contracts to
restore a property, that is [[sliding-window]]. It shares the amortized argument
above and nothing else.

Here are the two dominance variants, checked against their own definitions:

```python run
import random


def max_area(h):
    """Container With Most Water: best (width x min-height) over all pairs."""
    lo, hi, best = 0, len(h) - 1, 0
    while lo < hi:
        best = max(best, (hi - lo) * min(h[lo], h[hi]))
        if h[lo] < h[hi]:
            lo += 1                      # column lo is dominated: retire it
        else:
            hi -= 1
    return best


def trap(h):
    """Trapping Rain Water in O(1) space: fill from whichever side is lower."""
    lo, hi = 0, len(h) - 1
    lmax = rmax = water = 0
    while lo < hi:
        if h[lo] < h[hi]:
            lmax = max(lmax, h[lo])
            water += lmax - h[lo]        # lmax is the binding constraint here
            lo += 1
        else:
            rmax = max(rmax, h[hi])
            water += rmax - h[hi]
            hi -= 1
    return water


def brute_area(h):
    return max([(j - i) * min(h[i], h[j])
                for i in range(len(h)) for j in range(i + 1, len(h))], default=0)


def brute_trap(h):
    return sum(min(max(h[:i + 1]), max(h[i:])) - h[i] for i in range(len(h)))


demo = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
print("heights   ", demo)
print("max_area  ", max_area(demo), "(brute force:", brute_area(demo), ")")
print("trapped   ", trap(demo), "(brute force:", brute_trap(demo), ")")

rng = random.Random(11)
for _ in range(600):
    h = [rng.randrange(0, 7) for _ in range(rng.randrange(0, 12))]
    assert max_area(h) == brute_area(h), h
    assert trap(h) == brute_trap(h), h
print("600 random skylines: both O(n) sweeps match the O(n^2) definitions")
```

## Recognising it in a statement

Signals, in descending order of reliability:

- **"sorted"** together with **"find a pair / triple summing to"**, or
  **"closest to"** — converging sweep, straight off the template. If the array is
  not sorted but the answer does not depend on position, sorting first is
  allowed and usually intended.
- **"in place"**, **"O(1) extra space"**, **"return the new length"** — the
  read/write pair. The phrase "the judge only checks the first `k` elements" is
  the same signal in disguise.
- **two already-sorted inputs** and an output that is a merge, intersection or
  difference — one pointer per input.
- **"palindrome"**, **"reads the same forwards and backwards"**, **"from both
  ends"** — converging on equality.
- **maximise something over a pair of indices** where the score improves with
  width and is capped by the weaker endpoint — dominance elimination.
- The constraint line says `n <= 10⁵` or `2·10⁵` and the obvious algorithm is
  quadratic, while there is an ordering you could exploit. `n log n` or `n` is
  the intended shape, and when the data is already ordered the sweep is usually
  the missing piece.

The anti-signals matter as much:

- **Unsorted and you must report original indices.** Sorting loses them; carrying
  `(value, index)` pairs works but a hash map is simpler and linear.
- **You need the `k`-th best pair, not the best.** Elimination gives you one
  extreme, not a ranking — that is [[heap]] or [[quickselect]] territory.
- **The scoring function is not monotone along the sweep.** If moving `lo` can
  make a previously-dead column alive again, there is no elimination and the
  pointers have nothing to stand on.
- **"Count subarrays with at most k distinct"** and similar — two indices, yes,
  but the left pointer chases a *property of the window*, not an eliminated
  column. [[sliding-window]].

## Traps

**`while lo <= hi` in a converging loop.** Symptom: an element pairs with itself
and you report a pair that does not exist. Demonstrated below.

**Moving only one pointer after a match when you are enumerating.** Symptom: the
same triplet appears four or six times in the output. Demonstrated below.

**Forgetting to skip duplicate *values*, not duplicate *indices*.** Symptom:
`[-2, 0, 0, 2, 2]` yields `(-2, 0, 2)` twice even though both pointers moved. The
fix is a `while` that walks past every equal neighbour, at the outer index too.

**Sorting when order carries meaning.** Symptom: correct pair, wrong indices, or
a "preserve the relative order" requirement quietly violated — *Alternate
Positive and Negative Values* states that requirement explicitly, and a sort
destroys it.

**Overwriting unread data in an in-place merge.** Symptom: correct on some
inputs, scrambled on others. In *Merge Sorted Array* the answer is to fill from
the back, where the free space is, so the write pointer is always ahead of both
read pointers.

**Dropping the tail.** Symptom: output shorter than `len(a) + len(b)`, and only
when one input is exhausted early. Always flush both remainders.

**Moving the wrong side in a dominance sweep.** Symptom: *Trapping Rain Water*
returns a plausible-but-too-large number on skylines whose tall bar is on the
right. Move the *lower* side; the proof in the note above is the reason.

**Assuming the pointers bound a meaningful window.** In a converging sweep the
region between `lo` and `hi` is "not yet eliminated", not "a candidate answer".
Reading it as a window is how a converging problem gets solved with sliding-window
code that passes the samples and fails everything else.

```python run
def pair_loose(a, t):                 # WRONG: <= lets one element pair with itself
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        s = a[lo] + a[hi]
        if s == t:
            return (lo, hi)
        lo, hi = (lo + 1, hi) if s < t else (lo, hi - 1)
    return None


def pair_strict(a, t):                # RIGHT
    lo, hi = 0, len(a) - 1
    while lo < hi:
        s = a[lo] + a[hi]
        if s == t:
            return (lo, hi)
        lo, hi = (lo + 1, hi) if s < t else (lo, hi - 1)
    return None


def three_sum_naive(a):               # WRONG: emits the same triplet many times
    a = sorted(a)
    out = []
    for i in range(len(a) - 2):
        lo, hi = i + 1, len(a) - 1
        while lo < hi:
            s = a[i] + a[lo] + a[hi]
            if s < 0:
                lo += 1
            elif s > 0:
                hi -= 1
            else:
                out.append((a[i], a[lo], a[hi]))
                lo += 1                # only one side moved past the match
    return out


def three_sum(a):                     # RIGHT: skip equal neighbours at every level
    a = sorted(a)
    out = []
    for i in range(len(a) - 2):
        if i and a[i] == a[i - 1]:
            continue
        lo, hi = i + 1, len(a) - 1
        while lo < hi:
            s = a[i] + a[lo] + a[hi]
            if s < 0:
                lo += 1
            elif s > 0:
                hi -= 1
            else:
                out.append((a[i], a[lo], a[hi]))
                lo += 1
                hi -= 1                # both, or the next probe repeats the match
                while lo < hi and a[lo] == a[lo - 1]:
                    lo += 1
    return out


a = [1, 3, 4, 6]
print("pair_loose ([1,3,4,6], 8) ->", pair_loose(a, 8), "= 4 + 4, one element used twice")
print("pair_strict([1,3,4,6], 8) ->", pair_strict(a, 8), "= no such pair")
nums = [-2, 0, 0, 2, 2, -2, 1, 1]
print("three_sum_naive:", three_sum_naive(nums))
print("three_sum      :", three_sum(nums))
assert pair_loose(a, 8) == (2, 2) and pair_strict(a, 8) is None
assert sorted(set(three_sum_naive(nums))) == sorted(three_sum(nums))
assert len(three_sum(nums)) == len(set(three_sum(nums)))
print("naive emits", len(three_sum_naive(nums)), "triplets for",
      len(three_sum(nums)), "distinct ones")
```

## What to memorise

Two skeletons and one question.

```python
lo, hi = 0, len(a) - 1        # converging
while lo < hi:
    if <the (lo, hi) probe rules out everything in column lo>:
        lo += 1
    else:
        hi -= 1

w = 0                         # read / write
for r in range(len(a)):
    if keep(a[r]):
        a[w] = a[r]; w += 1   # a[0..w-1] is the finished answer
```

**The question** that turns a problem into the first skeleton: *"When I compare
these two ends, does the verdict kill one of them for every remaining partner?"*
If yes, move that one. If the verdict only tells you about this exact pair, you
do not have a two-pointer problem; you have a nested loop with hope.

**The habit**: before running the loop, say what each pointer means as a claim,
not as a location. Not "left and right" — "`lo` is the smallest index not yet
proven useless" and "`a[0..w-1]` is the part of the answer I have committed to".
If you cannot say it, the duplicate case will be wrong.

Numbers worth carrying: at `n = 2·10⁵` the pair count is `2·10¹⁰` and the sweep
count is `2·10⁵`. Total pointer movement in any of these loops is at most `2n`,
which is the only bound you need to quote in an interview.

## Check yourself

:::check
In *Container With Most Water* with `h = [1, 8, 6, 2, 5, 4, 8, 3, 7]`, the
pointers start at the two 1-and-7 ends and the first move retires index 0. Why is
it safe to discard *every* remaining pair that contains index 0, when we have
only measured one of them?
--
Because `h[0] = 1` is the shorter of the two ends, and height is capped by the
shorter side. For any `j` with `0 < j < 8`, the area of `(0, j)` is
`(j - 0) * min(h[0], h[j]) <= j * h[0]`, and `j < 8`, so that is strictly less
than `8 * h[0] = area(0, 8)`, which we just computed. Every unmeasured pair in
column 0 is provably worse than a pair we already recorded, so the maximum cannot
be hiding there.

Note the shape of the argument: we did not measure those pairs, we *bounded*
them. That is what an elimination rule is, and every converging two-pointer
proof has one.
:::

:::check
Someone says "two pointers requires a sorted array". Where are they wrong, and
what is the correct statement?
--
They have mistaken the most common source of the property for the property
itself. The correct statement is: **each move must eliminate a whole family of
candidate pairs, and you must be able to prove it eliminates only pairs that
cannot be the answer.**

Sorting is one way to get there, and the most common one. But *Trapping Rain
Water* and *Container With Most Water* work on arbitrary skylines; *Interval List
Intersections* needs each list sorted, not the union; *Valid Palindrome II*
compares characters at the two ends of unsorted text; the read/write compaction
in *Filter Odds and Reverse Evens* has no order requirement at all. Conversely, a
perfectly sorted array with a non-eliminating question — "is there a pair whose
product is a perfect square?" — gives two pointers nothing to stand on, because
`a[lo] * a[hi]` being too small does not bound `a[lo] * a[j]` usefully in the
presence of negatives.
:::

:::check
In the in-place compaction, why is `w <= r` at every step, and what would break
if it were not?
--
`w` starts at or below `r` and increases at most once per iteration, while `r`
increases exactly once per iteration, so `w` can never overtake `r`. That is a
loop invariant, provable by induction on the iteration count.

It matters because the write at `a[w] = a[r]` clobbers whatever was at index `w`.
While `w <= r`, the clobbered slot is one the reader has already passed, so no
unread input is destroyed. If a rule ever advanced `w` twice in one step, `w`
could pass `r` and you would overwrite an element before reading it — the bug
whose symptom is "correct on my example, garbage on the judge". The same
reasoning is why *Merge Sorted Array* fills from the back: that is where the
guarantee "the write pointer is ahead of both read pointers" holds.
:::

:::check
*3Sum* is described as `O(n²)`, yet it begins with a sort. Derive the bound and
explain why the sort does not appear in it. Then say why the hash-map trick that
makes two-sum linear does not make 3Sum linear.
--
Sorting costs `Θ(n log n)`. The outer index `i` runs over `n - 2` values, and for
each one the converging sweep does at most `(n - i - 1)` probes because
`hi - lo` starts at `n - i - 2` and falls by one per iteration. The total is
`Σᵢ₌₀ⁿ⁻³ (n - i - 1) = Θ(n²)`. Since `n log n` is asymptotically smaller than
`n²`, the sum `Θ(n log n) + Θ(n²)` is `Θ(n²)`; the sort is real work but it is
not the bound.

The hash map removes a factor of `n` from the *innermost* search, not from the
outer enumeration. Two-sum has one free index, so replacing the inner scan with a
lookup gives `Θ(n)`. 3Sum has two free indices; a hash map still leaves you
enumerating pairs, so it is `Θ(n²)` as well — with `Θ(n)` extra space, worse
duplicate handling, and no ordering to lean on. Sorting plus the sweep is the
better version of the same bound.
:::

:::check
A candidate solves "count the number of pairs `i < j` with `a[i] + a[j] == t`" in
a sorted array by running the converging loop and, on every match, incrementing
the count and doing `lo += 1; hi -= 1`. They test on `[1, 2, 3, 4]` with `t = 5`
and get 2, which is right. Where does this break?
--
It breaks on duplicates, which `[1, 2, 3, 4]` does not have. Take
`a = [1, 1, 1, 4, 4]` with `t = 5`. The true count is 6: three 1s each paired
with two 4s. Their loop probes `(0, 4)` — a match, count 1 — then moves to
`(1, 3)`, another match, count 2, then `lo = 2, hi = 2` and the loop ends. It
reports 2.

The invariant is still intact — nothing good was discarded by a *comparison* —
but the `s == t` branch is not a comparison, it is an enumeration step, and
advancing one index from each side silently skips the cross pairs. The fix is to
count blocks: when `a[lo] == a[hi]`, the whole remaining window is one value and
the answer gains `m(m-1)/2` for `m = hi - lo + 1`; otherwise count the run of
equal values at each end, `p` and `q`, add `p * q`, and jump both pointers past
their runs. The general lesson is the fifth assumption from the proof: the
elimination argument justifies the *no* branches, and the *yes* branch always
needs its own reasoning.
:::
