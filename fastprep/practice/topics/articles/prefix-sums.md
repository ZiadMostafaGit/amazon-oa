# Prefix Sums and Difference Arrays

> A prefix sum pays once, up front, for every range question you will ever ask,
> because addition has an inverse — and the difference array is the same trick
> run backwards, so that writing to a whole range costs two numbers.

## When you reach for it

You reach for prefix sums when a problem is **read-heavy over ranges of a fixed
array**: the data does not change, and you are asked about contiguous stretches
of it over and over. *Circular Route Query Distance* hands you the distances
between consecutive bus stops and then asks, for many pairs of stops, how far
apart they are. Answering one query by walking the stops is fine. Answering
100,000 of them that way is 10^10 additions, and the constraint line telling you
"an efficient solution should precompute prefix sums around the circle" is
unusually blunt about it.

You reach for a **difference array** when the asymmetry points the other way:
**write-heavy over ranges, read once at the end**. *Maximum User Traffic* gives
you login and logout days for up to 100,000 users and asks how many days carry
the peak load. Every user adds 1 to a contiguous block of days. Doing that block
by block is again quadratic; doing it as two writes per user is linear.

Those two shapes — many range reads of static data, many range writes then one
read — are the same idea seen from opposite ends, and between them they account
for 162 problems in this bank, which puts the topic at #25 of 150. The families:

- **A running total is literally the answer.** *Wallet Balance on a Selected
  Day*, *Find First Index Where Prefix Sum Becomes Non-Positive*, *Minimum Start
  Value*.
- **Split the array in two and compare the halves.** *Balanced Sum* wants the
  pivot where left sum equals right sum; *Find Fair Indexes* wants an index
  where four sums, across two arrays, are all equal.
- **Many range queries, static data.** *Circular Route Query Distance*, *Has
  Vowels*, *Get Success Value*.
- **Count subarrays with a property.** *Count Subarrays with a Target Sum* and
  *Maximum Number of Workers with Equal Left and Right Shoes* are both "two
  prefix sums are equal" in disguise.
- **Range updates, one readout.** *Range Negation Updates*, *Maximum User
  Traffic*, *Focus on Efficiency*.

The tool is **wrong** in three situations, and each has a better answer.

If the array is **mutated between queries**, a prefix sum is stale the moment
you touch an element, and rebuilding costs O(n) per update. That is what
[[fenwick-tree]] and [[segment-tree]] exist for.

If the range aggregate is **not invertible** — minimum, maximum, greatest common
divisor — there is no subtraction to do. `min` over `[l, r]` cannot be recovered
from `min` over two prefixes, and no cleverness with a single array fixes it.
You want [[sparse-table]], [[segment-tree]] or [[monotonic-deque]].

And if the values are all **non-negative** and you only need one window at a
time, a [[sliding-window]] answers in O(1) extra space. *Longest Subarray* asks
for the longest stretch summing to at most `k` with `1 <= a[i] <= 10^3`; the
positivity is exactly what makes the two-pointer version legal. Read the sign
constraint before you choose.

## The idea

**Put milestone markers on the road, and measure any stretch by subtracting two
markers.**

That is the whole chapter. Let `P[i]` be the distance from the start of the road
to marker `i` — in array terms, the sum of the *first `i`* elements. Then the
sum of `a[l..r]` is `P[r+1] - P[l]`: the total up to the far end, minus the total
up to the near end, because the part you subtract is exactly the part you did not
want.

<svg viewBox="0 0 680 250" role="img" aria-label="an array with its prefix-sum markers on the boundaries between cells, and a bracket showing that a range sum is the difference of two markers">
  <g>
    <rect x="60" y="36" width="80" height="44" rx="4"/>
    <rect class="fill" x="140" y="36" width="80" height="44" rx="4"/>
    <rect class="fill" x="220" y="36" width="80" height="44" rx="4"/>
    <rect class="fill" x="300" y="36" width="80" height="44" rx="4"/>
    <rect x="380" y="36" width="80" height="44" rx="4"/>
    <rect x="460" y="36" width="80" height="44" rx="4"/>
    <text x="100" y="64" text-anchor="middle">3</text>
    <text x="180" y="64" text-anchor="middle">-1</text>
    <text x="260" y="64" text-anchor="middle">4</text>
    <text x="340" y="64" text-anchor="middle">-1</text>
    <text x="420" y="64" text-anchor="middle">5</text>
    <text x="500" y="64" text-anchor="middle">-9</text>
    <text x="20" y="64">a</text>
    <line x1="60" y1="84" x2="60" y2="112"/>
    <line x1="140" y1="84" x2="140" y2="112"/>
    <line x1="220" y1="84" x2="220" y2="112"/>
    <line x1="300" y1="84" x2="300" y2="112"/>
    <line x1="380" y1="84" x2="380" y2="112"/>
    <line x1="460" y1="84" x2="460" y2="112"/>
    <line x1="540" y1="84" x2="540" y2="112"/>
    <text x="60" y="128" text-anchor="middle">P0</text>
    <text x="140" y="128" text-anchor="middle">P1</text>
    <text x="220" y="128" text-anchor="middle">P2</text>
    <text x="300" y="128" text-anchor="middle">P3</text>
    <text x="380" y="128" text-anchor="middle">P4</text>
    <text x="460" y="128" text-anchor="middle">P5</text>
    <text x="540" y="128" text-anchor="middle">P6</text>
    <text x="60" y="148" text-anchor="middle">0</text>
    <text x="140" y="148" text-anchor="middle">3</text>
    <text x="220" y="148" text-anchor="middle">2</text>
    <text x="300" y="148" text-anchor="middle">6</text>
    <text x="380" y="148" text-anchor="middle">5</text>
    <text x="460" y="148" text-anchor="middle">10</text>
    <text x="540" y="148" text-anchor="middle">1</text>
    <line x1="140" y1="182" x2="380" y2="182"/>
    <line x1="140" y1="182" x2="140" y2="170"/>
    <line x1="380" y1="182" x2="380" y2="170"/>
    <text x="260" y="204" text-anchor="middle">a[1..3]</text>
    <text x="260" y="228" text-anchor="middle">P4 - P1 = 5 - 3 = 2</text>
    <text x="20" y="128">P</text>
  </g>
</svg>

Notice where the markers live: **on the boundaries between cells, not on the
cells**. There are `n` cells and `n + 1` boundaries, which is why `P` has one
more entry than `a` and why `P[0] = 0` is not decoration. `P[0]` is the sum of
the empty prefix, and its presence is what makes `P[r+1] - P[l]` correct when
`l = 0` without a special case. Nearly every off-by-one in this topic is
someone putting the markers on the cells.

The second half of the idea is the inverse map. If `P` is a discrete integral,
the **difference array** `D[i] = a[i] - a[i-1]` is a discrete derivative, and the
two undo each other: the running sum of `D` reconstructs `a`. Adding a constant
`v` to a whole stretch of `a` changes its derivative in exactly two places — up
by `v` where the stretch starts, back down by `v` just past where it ends. So a
range update becomes `D[l] += v; D[r+1] -= v`, two writes however long the range,
and one final pass turns `D` back into the array everyone wanted.

## Worked by hand

Take `a = [3, -1, 4, -1, 5, -9]`, the array in the diagram. Build `P` with the
loop `P[i+1] = P[i] + a[i]`, starting from `P[0] = 0`.

| step `i` | `a[i]` | computed | `P` so far |
| --- | --- | --- | --- |
| — | — | `P[0] = 0` | `[0]` |
| 0 | 3 | `P[1] = 0 + 3` | `[0, 3]` |
| 1 | -1 | `P[2] = 3 + (-1)` | `[0, 3, 2]` |
| 2 | 4 | `P[3] = 2 + 4` | `[0, 3, 2, 6]` |
| 3 | -1 | `P[4] = 6 + (-1)` | `[0, 3, 2, 6, 5]` |
| 4 | 5 | `P[5] = 5 + 5` | `[0, 3, 2, 6, 5, 10]` |
| 5 | -9 | `P[6] = 10 + (-9)` | `[0, 3, 2, 6, 5, 10, 1]` |

Now answer three queries with no further additions:

| query | formula | arithmetic | check by hand |
| --- | --- | --- | --- |
| sum `a[1..3]` | `P[4] - P[1]` | `5 - 3` = 2 | `-1 + 4 - 1` = 2 |
| sum `a[0..5]` | `P[6] - P[0]` | `1 - 0` = 1 | the whole array = 1 |
| sum `a[4..4]` | `P[5] - P[4]` | `10 - 5` = 5 | `a[4]` = 5 |

Then the difference array, on the same data. Suppose the array starts as six
zeros and we apply two range updates: add 3 to `[1, 3]`, then add 2 to `[2, 5]`.
`D` has seven slots so that `r + 1 = 6` has somewhere to land.

| step | action | `D` after |
| --- | --- | --- |
| start | — | `[0, 0, 0, 0, 0, 0, 0]` |
| add 3 to `[1,3]` | `D[1] += 3`, `D[4] -= 3` | `[0, 3, 0, 0, -3, 0, 0]` |
| add 2 to `[2,5]` | `D[2] += 2`, `D[6] -= 2` | `[0, 3, 2, 0, -3, 0, -2]` |
| accumulate | running sum of `D[0..5]` | array = `[0, 3, 5, 5, 2, 2]` |

Check one cell by hand: index 2 was touched by both updates, so it should be 5.
It is. Index 4 was touched only by the second, so it should be 2. It is.

Three things the trace shows that reading the code would not.

**The table of `P` is one longer than the array, and the extra entry is at the
front.** Every query above uses an index one larger than the one you would
naively write: `sum a[1..3]` uses `P[4]`, not `P[3]`. Internalise "`P[i]` = sum
of the first `i` elements" rather than "sum up to index `i`" and the `+1` writes
itself.

**`P` is not monotone here.** It goes 0, 3, 2, 6, 5, 10, 1 — up and down,
because the array has negatives. That single observation kills a whole class of
wrong solutions: you cannot binary-search `P`, and you cannot grow a sliding
window and assume the sum only increases. When every `a[i] >= 0`, `P` *is*
non-decreasing and both of those become legal. The sign of the input is a
structural fact, not a detail.

**In the difference table, the two updates never interacted.** The second did not
need to know about the first; it wrote two slots and left. That is not luck — it
is the linearity of the derivative, and it is why the order of updates is
irrelevant and why you can accumulate a million before looking at the result.

## Why it is correct

Two claims need proof: that the build loop produces what we say it does, and
that the subtraction answers the question. Then the same for the difference
array, which is the first claim run in reverse.

:::proof Prefix sums answer range queries
**Setup.** Let `a[0..n-1]` be elements of a group under `+` — for our purposes,
the integers. Define the loop

```
P[0] = 0
for i = 0 .. n-1:  P[i+1] = P[i] + a[i]
```

**Invariant.** At the top of the iteration with counter `i`, for every `j <= i`
we have `P[j] = a[0] + a[1] + ... + a[j-1]`, the sum of the first `j` elements
(the empty sum, 0, when `j = 0`).

**Base case.** Before the first iteration, `i = 0` and the only `j <= 0` is
`j = 0`. `P[0]` was set to 0, which is the empty sum. The invariant holds.

**Inductive step.** Assume the invariant at the top of iteration `i`. The body
computes `P[i+1] = P[i] + a[i]`; by the invariant `P[i]` is the sum of the first
`i` elements, so `P[i+1] = (a[0] + ... + a[i-1]) + a[i]`, which by associativity
is the sum of the first `i+1` elements. Entries `P[j]` for `j <= i` are never
written again, so the invariant holds at the top of iteration `i+1`.

**Termination.** The counter `i` increases by exactly 1 each pass and the loop
stops at `i = n`, so it performs `n` iterations and halts. On exit the invariant
holds for all of `P`.

**The query theorem.** Fix `0 <= l <= r <= n-1`. The index set `{0, ..., r}` is
the disjoint union of `{0, ..., l-1}` and `{l, ..., r}`, and these are
consecutive blocks, so by associativity

`P[r+1] = a[0] + ... + a[r] = (a[0] + ... + a[l-1]) + (a[l] + ... + a[r]) = P[l] + S`

where `S` is the sum we want. Every element of the group has an additive
inverse, so we may add `-P[l]` to both sides: `S = P[r+1] - P[l]`. ∎

**The difference array.** Define `D[0] = a[0]` and `D[i] = a[i] - a[i-1]` for
`1 <= i <= n-1`. Claim: the running sum `S_k = D[0] + ... + D[k]` equals `a[k]`.
Induction on `k`: `S_0 = D[0] = a[0]`; and `S_{k+1} = S_k + D[k+1] = a[k] +
(a[k+1] - a[k]) = a[k+1]`. The sum telescopes.

**Range update.** Let `a'` be `a` with `v` added to every index in `[l, r]`,
that is `a'[i] = a[i] + v·1[l <= i <= r]`. Then for `i >= 1`,

`D'[i] = a'[i] - a'[i-1] = D[i] + v·(1[l <= i <= r] - 1[l <= i-1 <= r])`

The bracketed difference is `+1` exactly when `i = l`, `-1` exactly when
`i = r+1`, and 0 everywhere else — because the two indicator windows are the
same window shifted by one, so they agree except at the two edges. (The `i = 0`
case is the same statement with the convention `a'[-1] = 0`.) Therefore
`D' = D` except for `D[l] += v` and `D[r+1] -= v`: two writes.

**Composition.** The map `a ↦ D` is linear, and each update adds a fixed vector
to `D` that depends only on `(l, r, v)`. Vector addition is commutative and
associative, so applying `k` updates in any order gives the same `D`, and hence
the same reconstructed array. ∎
:::

Now the part worth more than the proof: **what did it assume?**

- **Additive inverses exist.** The query theorem used `-P[l]`. Minimum, maximum
  and gcd have no inverse, so the subtraction step is unavailable — not a gap in
  the argument, but a theorem about where the trick stops.
- **Associativity, and it must be exact.** IEEE floating-point addition is *not*
  associative, so `P[r+1] - P[l]` on floats differs from the honestly-summed
  range, and the error grows with the length of the prefix. *Online No-Intercept
  Linear Regression* maintains running sums of `x·y` and `x²` and is graded to
  10^-6 for exactly this reason. See [[numerical-stability]].
- **The array does not change after the build.** The invariant is about `a` as
  it was during the loop. Mutate `a` afterwards and `P` describes a history that
  no longer exists.
- **The index `r+1` is in range.** The theorem is stated for `r <= n-1`, so
  `r+1 <= n`, so `P` must have `n+1` slots. Likewise `D` must have `n+1` slots
  so that an update ending at the last index has somewhere to write its `-v`.
- **No overflow.** With `n = 10^5` and `|a[i]| <= 10^9`, `P` can reach 10^14 —
  four orders of magnitude past a 32-bit integer. *Get Success Value* spells it
  out, and *Count Subarrays with a Target Sum* says the prefix sums are
  accumulated in signed 64-bit. Python is immune ([[big-integers]]); the
  language you write this in during an onsite may not be.

Four of the five common bugs in this topic are one of those assumptions quietly
failing. The fifth is the `+1`.

## What it costs

**Build.** The loop body is one addition and one store, O(1), executed exactly
`n` times. Total `Θ(n)` time. There is no recurrence to solve — this is a
counting argument: `n` iterations times constant work.

**Query.** Two array reads and a subtraction: `Θ(1)`, with no hidden constant.

**`q` queries after the build:** `Θ(n + q)`, against `Θ(n·q)` for the honest
scan. Divide to see when it pays: amortised over the queries, the preprocessing
adds `n/q` per query, so the average cost per query is `1 + n/q`. With
`n = q = 10^5` that is 2 operations per query instead of 50,000. With `q = 1` it
is `n + 1` — no better than scanning, which is the real answer to "is it always
worth it?": no, it is worth it when `q` is not tiny.

**Space.** `n + 1` integers. If you may destroy the input, build `P` in place
with `a[i] += a[i-1]` for `Θ(1)` extra — but then `sum(l..r)` is `a[r] - a[l-1]`
with a special case for `l = 0`, and you have traded a special case for a
kilobyte. Usually a bad trade.

**Lower bound, which tells you when to stop optimising.** Any correct algorithm
must read every element during preprocessing. Suppose it never reads `a[i]`; run
it on `a`, and again on `a` with `a[i]` increased by 1. Its state is identical in
both runs, so it gives the same answer to the query `[i, i]` — but the correct
answers differ by 1. So `Ω(n)` preprocessing is unavoidable, and `Θ(n)` build
with `Θ(1)` query is optimal for static range sums.

**Difference array.** `k` updates at `Θ(1)` each, plus one `Θ(n)` accumulation
pass: `Θ(n + k)` total, `Θ(n)` space. Against `Θ(n·k)` naive. *Maximum User
Traffic* has `n` up to 10^5 users over days up to 10^5, so naive is 10^10 and
this is 2·10^5.

**The costs people forget.** The **hash map** in the count-subarrays variant is
`Θ(n)` *expected*, not worst case — adversarial keys collide, and it allocates
one entry per distinct prefix value ([[hash-tables]]). The **two-dimensional**
table answers a rectangle query in four lookups, genuinely O(1), but needs
`(n+1)·(m+1)` cells: for a 10^4 × 10^4 grid that is 10^8 integers and will not
fit. And the **sort**, when there is one: *Get Success Value* is
`Θ(n log n + q)`, where the `log n` is the sort, not the prefix sums.

## The implementation

```python run
def build(a):
    """P[i] = sum of the FIRST i elements.  len(P) == len(a) + 1, P[0] == 0."""
    P = [0] * (len(a) + 1)
    for i, x in enumerate(a):
        P[i + 1] = P[i] + x
    return P


def range_sum(P, l, r):
    """Sum of a[l..r], inclusive."""
    return P[r + 1] - P[l]


def count_subarrays_with_sum(a, target):
    """How many contiguous a[l..r] sum to target.  Works with negatives."""
    seen = {0: 1}                 # the empty prefix: without it, l == 0 is lost
    running = total = 0
    for x in a:
        running += x
        total += seen.get(running - target, 0)
        seen[running] = seen.get(running, 0) + 1
    return total


a = [3, -1, 4, -1, 5, -9, 2]
P = build(a)
print("a =", a)
print("P =", P, " (one longer than a)")

for l, r in [(0, 0), (1, 3), (4, 4), (0, 6)]:
    got = range_sum(P, l, r)
    assert got == sum(a[l:r + 1]), (l, r, got)
    print("sum a[%d..%d] = P[%d] - P[%d] = %3d" % (l, r, r + 1, l, got))

n = len(a)
for l in range(n):                       # every range, against the honest answer
    for r in range(l, n):
        assert range_sum(P, l, r) == sum(a[l:r + 1])
print("all", n * (n + 1) // 2, "ranges agree with brute force")

for t in (-1, 0, 2, 7, 100):
    brute = sum(1 for l in range(n) for r in range(l, n) if sum(a[l:r + 1]) == t)
    fast = count_subarrays_with_sum(a, t)
    assert fast == brute, (t, fast, brute)
    print("subarrays summing to %4d: %d" % (t, fast))
```

Three lines are doing the work.

`P = [0] * (len(a) + 1)` — the allocation *is* the algorithm's correctness
argument. One extra slot, initialised to the additive identity. Because it
exists, `range_sum` has no branch, and a function with no branch has no branch to
get wrong.

`total += seen.get(running - target, 0)` — the query theorem read backwards. A
subarray ending here sums to `target` exactly when some earlier prefix equals
`running - target`. So instead of searching for subarrays, count matching
prefixes. That reframing is the most reusable idea in this chapter: *"subarray
with property X" becomes "pair of prefix values with relation X"*. It is why
*Maximum Number of Workers with Equal Left and Right Shoes* is a prefix-sum
problem — map `L` to `+1` and `R` to `-1`, and an interval with equal counts is
an interval summing to zero, which is a pair of equal prefix values.

`seen = {0: 1}` — the same empty prefix as `P[0]`, in map form. Seed it and
subarrays that start at index 0 are counted; forget it and they are not, which
produces an answer that is *almost* right, the worst kind of wrong.

Now the other direction.

```python run
def range_add(n, updates):
    """Apply each (l, r, v) as 'add v to a[l..r]', then materialise the array."""
    D = [0] * (n + 1)              # n + 1 so that r + 1 == n has a home
    for l, r, v in updates:
        D[l] += v
        D[r + 1] -= v
    out, run = [], 0
    for i in range(n):
        run += D[i]
        out.append(run)
    return out


n = 8
updates = [(1, 4, 3), (0, 7, 1), (4, 4, -5), (2, 6, 2)]

naive = [0] * n
for l, r, v in updates:
    for i in range(l, r + 1):
        naive[i] += v

fast = range_add(n, updates)
print("updates :", updates)
print("naive   :", naive)
print("2 writes:", fast)
assert fast == naive

# order does not matter, because the updates just add vectors to D
assert range_add(n, list(reversed(updates))) == naive
print("reversed order gives the same array")

# 'how many days carry the peak load' -- the Maximum User Traffic shape
sessions = [(1, 3), (2, 5), (0, 2), (4, 6), (2, 2)]
span = max(r for _, r in sessions) + 1
traffic = range_add(span, [(l, r, 1) for l, r in sessions])
peak = max(traffic)
assert traffic == [1, 2, 4, 2, 2, 2, 1]
print("traffic :", traffic, "-> peak", peak, "on", traffic.count(peak), "day(s)")


def moves(target):
    """Fewest '+1 on a range' operations to build target from all zeros."""
    prev = total = 0
    for x in target:
        total += max(0, x - prev)    # every rise in the difference array
        prev = x
    return total


assert moves([0, 0, 0]) == 0 and moves([1, 2, 1]) == 2
print("moves to build [3,1,4,1,5]:", moves([3, 1, 4, 1, 5]))
```

The last function deserves a word, because it is *Focus on Efficiency* and looks
like a different problem. Each range-increment adds `+1` at one position of the
difference array and `-1` at another. The target's difference array has some
positive entries; each must be paid for by a distinct operation's `+1`, so the
number of operations is at least the sum of the positive differences — and that
many suffices, pairing each rise with a later fall. A one-line scan, visible only
if you are looking at the derivative instead of the array.

## Variants you will meet

**Prefix XOR.** XOR is its own inverse, so `xor(l..r) = X[r+1] ^ X[l]`. Same
template, different operator. See [[xor-tricks]].

**Prefix product.** Products form a group only when no element is zero, so the
division trick breaks on a single 0. The standard workaround — prefix product
from the left, suffix product from the right, multiply them around each index —
avoids division entirely.

**Prefix max and suffix max.** Not invertible, so no range queries; but the
*split-point* reading still works, because you only ever need "best to the left"
and "best to the right". *Get Max Aggregate Temperature Change* compares a prefix
sum against a suffix sum at every index; *Get Minimum Round Trip Cost* pairs each
departure with the cheapest later return, a suffix minimum; *Count Sortable
Splits* is prefix-max versus suffix-min; *Eating Candies* walks a prefix sum and
a suffix sum toward each other. Building one array left to right and one right to
left is the second most common use of this topic after range queries.

**Prefix counts of a predicate.** Replace each element by 1 if it satisfies some
test and 0 otherwise; the prefix sum now counts matches in a range. *Has Vowels*
is exactly this. Pairs naturally with [[frequency-counting]].

**Two-dimensional prefix sums.** `P[i][j]` is the sum of the whole rectangle
above-left of `(i, j)`; a rectangle query is
`P[r+1][c+1] - P[r+1][c0] - P[r0][c+1] + P[r0][c0]` — [[inclusion-exclusion]],
with the corner added back because it was subtracted twice. *Generate Matrix B*
asks for precisely this table as its output. See also [[matrix-traversal]].

**Circular prefix sums.** On a ring, the arc from `i` forward to `j` is
`P[j] - P[i]` when `i <= j`, and the other way round is `total` minus that.
*Circular Route Query Distance* and *Shortest Distance on a Circular Bus Route*
are both `min(arc, total - arc)` after one linear precomputation.

**Prefix sums modulo m.** Group the prefix values by residue: two prefixes with
the same residue bound a subarray whose sum is divisible by `m`. *Number of
Divisible Substrings* is the harder cousin, where the modulus is the length of
the window, so you fix the length first and bucket by residue mod that length.

**Prefix sums plus binary search.** Sort, prefix-sum, then answer each query in
O(log n). *Get Success Value* sorts descending so that "the top `k`" is a
prefix; *Minimum Operations Required* sorts ascending so that the cost of moving
every price to `q` splits into "everything below `q`" and "everything above
`q`", each a range sum located by [[binary-search]].

**Prefix sums with a running extreme.** Carry `min(P)` as you go. *Minimum Start
Value* is `1 - min(0, min prefix)`; [[kadane|Kadane's algorithm]] is
"best subarray ending here = `P[i+1] - min P[j] for j <= i`" in disguise.

**Difference arrays in 2D.** Four writes per rectangle update — `+v`, `-v`,
`-v`, `+v` at the corners — then a 2D prefix sum to materialise.

**Non-additive range updates.** *Range Negation Updates* flips signs on a range
rather than adding. Negation composes as a parity: track how many flips cover
each index with a `+1/-1` difference array and read the parity at the end. Any
update forming a group under composition can ride the same two-writes trick.

**When updates interleave with queries**, prefix sums collapse and you move to
[[fenwick-tree]] (point update, prefix query), [[segment-tree]] with
[[lazy-propagation]] (range update, range query), or [[sqrt-decomposition]].

**Interval endpoints as events.** A difference array is [[sweep-line]] on a
small integer axis. When the coordinates are large or not integers, sort the
`+1`/`-1` events instead of indexing them.

## Recognising it in a statement

Ordered by how reliable the signal is.

1. **"`q` queries, each `[l, r]`, on an array that never changes"**, with `n` and
   `q` both up to 10^5. `n·q = 10^10` is dead and `n + q = 2·10^5` is free. This
   is as close to a giveaway as this topic gets.
2. **"Add `v` to every element between `l` and `r`"**, repeated, with the array
   only printed at the end. Difference array. If instead you must answer a query
   *between* updates, it is a [[segment-tree]].
3. **"Cumulative", "running total", "balance after day `i`"** — the prefix sum
   is the answer, not a step toward it. *Wallet Balance on a Selected Day*.
4. **"Split into two contiguous parts such that ..."** — prefix from the left,
   suffix from the right, one pass to compare. *Balanced Sum*, *Find Fair
   Indexes*.
5. **"Number of subarrays whose sum is / is divisible by ..."** — prefix sums
   plus a [[hash-tables|hash map]] of prefix values. *Count Subarrays with a
   Target Sum*.
6. **"Equal numbers of X and Y in a contiguous block"** — map to `+1` and `-1`
   and look for equal prefix values. *Maximum Number of Workers with Equal Left
   and Right Shoes*.
7. **The constraint line insists on 64-bit output** while `n` and `|a[i]|` are
   both large. Someone is telling you a sum of many elements is involved.
8. **A brute force whose inner loop is a sum.** Any repeated inner summation
   over a prefix or a range is a prefix sum waiting to be extracted.

Anti-signals, which are just as useful:

- The aggregate is **min, max or gcd**. No inverse, no subtraction. Different
  chapter.
- The array is **modified between queries**. Prefix sums go stale.
- The word is **"subsequence"**, not "subarray" or "contiguous". Prefix sums are
  about contiguity; a subsequence problem is usually
  [[dynamic-programming|DP]].
- **All values are non-negative and you want one best window.** A
  [[sliding-window]] or [[two-pointers]] solution is shorter and uses no extra
  space. *Longest Subarray* and *Threshold Alerts* are both in that camp, and
  *Reduce Memory Usage* — delete the contiguous block of `m` processes that
  saves the most — is a fixed-width window you can do either way.

## Traps

**The `+1`.** `P[r] - P[l]` instead of `P[r+1] - P[l]`. Symptom: every answer is
short by exactly `a[r]`, and single-element queries return 0, which looks like a
different bug entirely.

**No `P[0] = 0`, or no `seen[0] = 1`.** Symptom: everything works except ranges
that start at index 0. Test `l = 0` first, always.

**`D` allocated with `n` slots.** Symptom: an `IndexError` on any update that
reaches the last element — or, in a language without bounds checking, silent
corruption. `n + 1` slots, every time.

**Overflow.** Symptom: sums correct on small inputs and negative on large ones.

**Mutating the array after building `P`.** Symptom: answers that were right in
your first test and wrong after you added an update step.

**Sliding a window over negative numbers.** Growing the window no longer
increases the sum, so "shrink while the sum is too big" has nothing to shrink
against. Symptom: correct on the sample, wrong on any test with a negative.

**2D sign errors.** Forgetting to add the corner back after subtracting the two
strips. Symptom: answers too small by exactly the overlap.

Here are the first two, side by side with the right versions.

```python run
a = [2, 7, 1, 8]
P = [0] * (len(a) + 1)
for i, x in enumerate(a):
    P[i + 1] = P[i] + x
print("a =", a, "  P =", P)

wrong_offset = P[2] - P[1]          # "P[r] - P[l]"
right_offset = P[3] - P[1]          # "P[r+1] - P[l]"
print("a[1..2] really is    :", sum(a[1:3]))
print("P[r]   - P[l] gives  :", wrong_offset, " <- short by a[r] = %d" % a[2])
print("P[r+1] - P[l] gives  :", right_offset)
assert right_offset == 8 and wrong_offset == 7
print("single element a[2..2]: wrong form gives", P[2] - P[2], "instead of", a[2])


def count_no_seed(a, t):
    seen, run, total = {}, 0, 0            # forgot the empty prefix
    for x in a:
        run += x
        total += seen.get(run - t, 0)
        seen[run] = seen.get(run, 0) + 1
    return total


def count_seeded(a, t):
    seen, run, total = {0: 1}, 0, 0
    for x in a:
        run += x
        total += seen.get(run - t, 0)
        seen[run] = seen.get(run, 0) + 1
    return total


b, t = [1, 2, 3, 0, 3], 3
n = len(b)
brute = sum(1 for l in range(n) for r in range(l, n) if sum(b[l:r + 1]) == t)
print("\nb =", b, " target", t)
print("brute force      :", brute)
print("without seed     :", count_no_seed(b, t), "<- misses every subarray starting at 0")
print("with seen[0] = 1 :", count_seeded(b, t))
assert count_seeded(b, t) == brute and count_no_seed(b, t) < brute
```

## What to memorise

Two templates, one sentence, one habit.

**The templates**, which should come out of your fingers without thought:

```python
P = [0] * (n + 1)
for i in range(n):
    P[i + 1] = P[i] + a[i]
# sum of a[l..r]  ==  P[r + 1] - P[l]

D = [0] * (n + 1)
D[l] += v; D[r + 1] -= v        # 'add v to a[l..r]', repeat as needed
a = list(itertools.accumulate(D))[:n]
```

**The sentence** that turns a problem into one of them: *"Am I reading many
ranges of an array that never changes, or writing many ranges and reading once?"*
First case, prefix sums. Second case, difference array. Neither, because the
reads and writes interleave — [[fenwick-tree]] or [[segment-tree]].

**The habit**: say `P[i]` out loud as *"the sum of the first `i` elements"*, never
as "the sum up to index `i`". The first phrasing makes `P[r+1] - P[l]` obvious
and `P[0] = 0` inevitable. The second phrasing is where the off-by-one is born.
The same habit in map form: the first thing you write is `seen = {0: 1}`.

Numbers worth carrying: a sum of 10^5 elements each up to 10^9 reaches 10^14, so
64-bit. `n·q = 10^10` is out of reach and `n + q = 2·10^5` is nothing. A 2D
prefix table over a 10^4 × 10^4 grid is 10^8 cells and will not fit.

And one structural fact: **the sign of the input decides the algorithm**. All
non-negative means `P` is monotone, which unlocks sliding windows and binary
search on `P`. Any negative value and you are in hash-map territory.

## Check yourself

:::check
Why does `P` have `n + 1` entries rather than `n`? Answer in terms of what the
entries *are*, not in terms of avoiding an error.
--
Because the entries are not attached to elements — they are attached to the
**boundaries between elements**, and `n` elements have `n + 1` boundaries.
`P[i]` is the total accumulated before you cross boundary `i`, i.e. the sum of
the first `i` elements. A range `a[l..r]` is the stretch of road between
boundary `l` and boundary `r+1`, so its length is `P[r+1] - P[l]`.

The empty prefix `P[0] = 0` is a real boundary — the one before the array
starts — and its value is the additive identity because the sum of no elements
is 0. Once you see it that way there is nothing to remember: the formula reads
off the picture, and the `l = 0` case needs no special handling because
boundary 0 exists like any other.
:::

:::check
Someone says: "prefix sums generalise to anything associative, so I'll build a
prefix-minimum array and answer range-minimum queries with it." Where are they
wrong, and what part of their claim is actually true?
--
The true part: building the array *is* fine. `M[i+1] = min(M[i], a[i])` is a
correct prefix minimum, and it answers "the minimum of the first `i` elements".

The wrong part is the query. Recovering the range answer needs
`P[r+1] = P[l] ⊕ S` to be solvable for `S`, which requires an **inverse**, not
just associativity. `min` has none, because the small element may lie entirely
in the discarded prefix. Concretely: `[1, 9, 9]` and `[1, 9, 1]` produce the
identical prefix-minimum array `[∞, 1, 1, 1]`, yet `min(a[1..2])` is 9 in one and
1 in the other. No arithmetic on `M[3]` and `M[1]` can tell them apart.

Prefix minima remain useful for split-point questions ("best to the left of
here"), not for arbitrary ranges. Those want a [[sparse-table]] or a
[[segment-tree]].
:::

:::check
In `count_subarrays_with_sum`, explain why counting *pairs of prefix values*
counts *subarrays*, and why the map must store multiplicities rather than a set
of values.
--
A subarray is determined by its two boundaries, so subarrays are in bijection
with pairs `(l, r+1)`, `l < r+1`. By the query theorem its sum is
`P[r+1] - P[l]`, so "subarray sums to `target`" is exactly "the two prefix values
differ by `target`". Scanning `r` left to right and asking how many earlier `l`
satisfy `P[l] = P[r+1] - target` counts every qualifying pair exactly once, at
its right boundary.

Multiplicities are required because prefix values repeat. In `[1, -1, 3]` with
`target = 3` the prefixes are `0, 1, 0, 3`, and 0 occurs twice — as the empty
prefix and again after index 1 — giving two valid subarrays, `[1,-1,3]` and
`[3]`. A set would record "0 has been seen" once and undercount.
:::

:::check
You apply a thousand range updates with a difference array and then reverse
their order and apply them again from scratch. Why must you get the identical
array, and what would have to be true of the updates for that to fail?
--
Each update `(l, r, v)` adds a fixed vector to `D` — `+v` in slot `l`, `-v` in
slot `r+1`, zero elsewhere — and that vector depends only on the update, never
on the current contents of `D`. The final `D` is the sum of those vectors plus
the initial one, and vector addition over the integers is commutative and
associative, so any order produces the same sum. Reconstruction is then a
deterministic function of `D`.

It fails as soon as an update's effect depends on the current values. "Multiply
`[l, r]` by 2" and "add 1 to `[l, r]`" do not commute. "Set `[l, r]` to `v`"
does not either — later assignments overwrite earlier ones, so order is the whole
answer. That is why range-assign needs a [[segment-tree]] with
[[lazy-propagation]] and not two writes. *Range Negation Updates* survives only
because negation composes as a parity, which *is* commutative: what matters is
how many flips cover each index, not which order they came in.
:::

:::check
A candidate says: "sliding windows beat prefix sums — same time, O(1) space, so
prefix sums are just the lazy version." Where are they wrong?
--
They are right in one narrow case and wrong in general.

The narrow case: for a **single** best-window question on a **non-negative**
array, a two-pointer window is `Θ(n)` time and `Θ(1)` space against the prefix
sum's `Θ(n)` space. *Longest Subarray*, with `1 <= a[i] <= 10^3`, is like this,
and the window is the better answer.

Where it breaks. First, **negatives**: a window works only if extending it moves
the sum monotonically, so that shrinking from the left is a meaningful repair.
With negatives, extending can lower the sum, the pointers have nothing to test,
and the technique has no correct form. Second, **many queries**: a window answers
one question per pass, so `q` arbitrary `[l, r]` queries cost `Θ(n·q)`, while the
prefix table is built once and each query is two reads. Third, **non-window
questions**: "how many subarrays sum to `k`" is not about one window at all.

They solve different problems that overlap on non-negative single-window
questions, and on that overlap the window is leaner.
:::
