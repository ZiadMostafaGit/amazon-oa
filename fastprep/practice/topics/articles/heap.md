# Binary Heaps and Priority Queues

> A heap is not a sorted container. It is the cheapest structure that knows one
> thing — who is next — and deliberately refuses to know anything else.

## When you reach for it

You reach for a heap when a problem repeatedly asks for the extreme element of a
set that **keeps changing**.

That last clause is the whole trigger. If the set is fixed, sort it once and walk
it; sorting is simpler and no slower. The heap earns its keep when elements
arrive and leave interleaved with the questions, so any sorted order you built
would be invalidated by the next arrival. Two hundred and three problems here use
one, which puts heaps at #20 of 150, in a few recognisable shapes:

- **Take the extreme, transform it, put it back.** *Last Stone Weight* smashes
  the two heaviest stones and reinserts the difference; *Connect N Ropes With
  Minimum Cost* joins the two shortest and reinserts the join. The set changes
  after every question, which is what sorting cannot survive.
- **The k best out of many.** *Top-K Using a Priority Queue* spells out the
  intended complexity, `O(n log k)`; *Top Ten Trades by Notional Value* states
  the memory too: "a heap that retains at most ten candidates instead of sorting
  the complete input". Own chapter: [[top-k]].
- **Scheduling and resource allocation.** *Meeting Rooms II*, *Minimum Number of
  Chairs*, *Assign Tasks to Servers*, *Assign Partitions to the Least-Loaded
  Servers*, *Single-Threaded CPU*. The heap holds *the resource that frees up
  soonest* or *the job that should run next* — often two heaps at once.
- **Merging sorted streams.** *Merge Three Sorted Arrays*, *K Smallest Elements
  from Sorted Arrays*: one live head per stream. See [[k-way-merge]].
- **Best-first search.** *Cheapest Flights Within K Stops*, *Find the Safest Path
  in a Grid*: the frontier is a heap keyed by cost so far. See [[dijkstra]].
- **Deterministic tie-breaking.** *Topological Sort with Secondary Ordering*
  replaces the ready-queue of [[topological-sort]] with a heap.

It is the wrong tool in four cases. For the k-th element **once**, from a fixed
set, [[quickselect]] is expected `O(n)`. For **rank** queries — "how many are
below x", "the predecessor of x" — a heap has no answer: [[ordered-set]] or
[[fenwick-tree]]. To **delete an arbitrary element** there is no operation at
all. And for a **sliding window** maximum, a monotonic deque is `O(n)`:
[[monotonic-stack]].

## The idea

A heap is a tournament bracket that is never fully played out.

Every node beats its children. Nothing is claimed about how two siblings compare,
or about two nodes in different subtrees. The champion is at the root
immediately, and everybody else sits in a partial order we have gone out of our
way not to resolve. That refusal is the source of the speed: sorting narrows `n!`
orderings to one, at `Θ(n log n)` comparisons however you do it, whereas a heap
pins down only the `n-1` parent-child relations.

The second half of the idea is that the bracket needs no pointers. Number the
nodes in level order — root 0, then its two children, then their four — and the
tree becomes an array with arithmetic instead of links:

```
parent(i) = (i - 1) // 2      left(i) = 2i + 1      right(i) = 2i + 2
```

<svg viewBox="0 0 660 300" role="img" aria-label="a five-node min-heap drawn as a tree above the array that stores it in level order">
  <g>
    <circle class="fill" cx="330" cy="40" r="22"/>
    <text x="330" y="46" text-anchor="middle">1</text>
    <circle cx="190" cy="115" r="22"/>
    <text x="190" y="121" text-anchor="middle">2</text>
    <circle cx="470" cy="115" r="22"/>
    <text x="470" y="121" text-anchor="middle">8</text>
    <circle cx="120" cy="185" r="22"/>
    <text x="120" y="191" text-anchor="middle">5</text>
    <circle cx="260" cy="185" r="22"/>
    <text x="260" y="191" text-anchor="middle">3</text>
    <line x1="203" y1="97" x2="317" y2="58"/>
    <line x1="457" y1="97" x2="343" y2="58"/>
    <line x1="133" y1="167" x2="177" y2="133"/>
    <line x1="247" y1="167" x2="203" y2="133"/>
    <rect x="180" y="225" width="60" height="38" rx="4"/>
    <rect x="240" y="225" width="60" height="38" rx="4"/>
    <rect x="300" y="225" width="60" height="38" rx="4"/>
    <rect x="360" y="225" width="60" height="38" rx="4"/>
    <rect x="420" y="225" width="60" height="38" rx="4"/>
    <text x="210" y="250" text-anchor="middle">1</text>
    <text x="270" y="250" text-anchor="middle">2</text>
    <text x="330" y="250" text-anchor="middle">8</text>
    <text x="390" y="250" text-anchor="middle">5</text>
    <text x="450" y="250" text-anchor="middle">3</text>
    <text x="210" y="283" text-anchor="middle">0</text>
    <text x="270" y="283" text-anchor="middle">1</text>
    <text x="330" y="283" text-anchor="middle">2</text>
    <text x="390" y="283" text-anchor="middle">3</text>
    <text x="450" y="283" text-anchor="middle">4</text>
    <text x="20" y="250">level order</text>
    <text x="20" y="283">index</text>
    <text x="20" y="40">every node</text>
    <text x="20" y="62">beats its</text>
    <text x="20" y="84">children</text>
  </g>
</svg>

Notice what that array is *not*: `[1, 2, 8, 5, 3]` is not sorted, its last cell
is not the maximum, and index 2 holds a bigger value than index 3. All that holds
is the constraint on the four parent-child pairs. No wasted space, no allocation
per element.

With the shape settled there are exactly two repairs to write. A value too small
for where it sits walks **up** until its parent is no larger. A value too large
walks **down**, swapping with the smaller of its two children, until both are no
smaller. Every heap operation is one of those two after a single cheap edit:
append, or overwrite the root.

## Worked by hand

Build a min-heap by pushing `5, 1, 8, 3, 2` in that order, then pop twice. The
middle column is the comparisons actually made.

| step | operation | comparisons | array after |
| --- | --- | --- | --- |
| 1 | push 5 | none — it is the root | `[5]` |
| 2 | push 1 | 1 vs parent 5: smaller, walk up | `[1, 5]` |
| 3 | push 8 | 8 vs parent 1: not smaller, stop | `[1, 5, 8]` |
| 4 | push 3 | 3 vs 5: up. 3 vs 1: stop | `[1, 3, 8, 5]` |
| 5 | push 2 | 2 vs 3: up. 2 vs 1: stop | `[1, 2, 8, 5, 3]` |
| 6 | pop → 1 | 3 to the root; children 2, 8, smaller is 2; 3 vs 2: down. child 5; 3 vs 5: stop | `[2, 3, 8, 5]` |
| 7 | pop → 2 | 5 to the root; children 3, 8, smaller is 3; 5 vs 3: down. no children | `[3, 5, 8]` |

Five things there are worth a second look, and none is visible in the code.

**The 8 never moved.** It landed at index 2 in step 3 and was still there in step
7 — the largest value in the set, one step from the root, which in a sorted array
would be an outrage. The heap does no work the questions did not force.

**The array is never sorted, at any point.** After step 5 it reads
`[1, 2, 8, 5, 3]`, and the last cell holds 3, not the maximum. If you ever write
`heap[-1]` expecting the largest element, this is the counterexample.

**Push and pop are not symmetric.** Walking up compares against one node, the
parent: about one comparison per level. Walking down must first decide *which*
child to descend into: about two. That ratio is why the combined "push then
immediately pop" — `heapreplace` / `heappushpop` — is worth reaching for in
*Top-K Using a Priority Queue*: one walk instead of two.

**In step 6 the value that went to the root came from the end of the array**, not
from either child — the only way to keep the shape complete, and the shape is
what makes the index arithmetic legal.

**Ties never move.** *Insert into a Min-Heap* states the rule explicitly —
"swap it with its parent while it is strictly smaller than that parent. Equal
values do not swap" — because the returned array depends on it. Both `<` and `<=`
maintain a valid heap; only one produces the array the grader wants.

### Building in one pass

Pushing one at a time is not the only way. Given `[5, 1, 8, 3, 2, 7]` already in
memory, run `sift_down` on every internal index — `0` to `n//2 - 1` — from the
last backwards, so `2, 1, 0`.

| i | value at i | its children | action | array after |
| --- | --- | --- | --- | --- |
| 2 | 8 | index 5 only: 7 | 8 > 7, swap down | `[5, 1, 7, 3, 2, 8]` |
| 1 | 1 | 3 and 2; smaller is 2 | 1 ≤ 2, stop | `[5, 1, 7, 3, 2, 8]` |
| 0 | 5 | 1 and 7; smaller is 1 | 5 > 1, swap down to index 1 | `[1, 5, 7, 3, 2, 8]` |
| 0 | 5 (now at 1) | 3 and 2; smaller is 2 | 5 > 2, swap down to index 4 | `[1, 2, 7, 3, 5, 8]` |

Three element moves to heapify six elements. That is what the code alone will not
tell you: almost every index is a leaf, and a leaf is already a valid heap of
one. Half the nodes are skipped, a quarter can fall at most one level, only the
root can fall the full height. Bottom-up is `Θ(n)`; `n` pushes is `Θ(n log n)`.

## Why it is correct

A data structure is correct when every operation preserves its representation
invariant and the invariant implies the answers it reports. State the invariant
exactly, then check each operation against it.

:::proof Every operation restores the heap property
**State.** An array `a[0..n-1]`. For `i >= 1`, `parent(i) = (i-1)//2`; the
children of `i` are `2i+1` and `2i+2` when those are less than `n`.

**Shape invariant (S).** The elements occupy exactly `0..n-1`, no gaps. Since the
index map defines the tree, a contiguous prefix of indices *is* a complete binary
tree, so (S) holds automatically as long as we only append at the end and remove
from the end.

**Order invariant (H).** For every `i` with `1 <= i < n`, `a[parent(i)] <= a[i]`.

**Claim A — what (H) buys.** If (H) holds then `a[0] = min(a)`. Induct on
`depth(i)`, the number of parent steps from `i` to `0`. Depth 0: `a[0] <= a[0]`.
Depth `d > 0`: `p = parent(i)` has depth `d-1`, so `a[0] <= a[p]` by hypothesis
and `a[p] <= a[i]` by (H); transitivity gives `a[0] <= a[i]`. Nothing is claimed
about siblings, or about which leaf is largest.

**Base case.** An array of length 0 or 1 satisfies (H) vacuously.

**Operation `push(x)`: append at index `m = n`, then sift up.** Appending can
break (H) only at the pair `(parent(m), m)`; every other pair is untouched. Let
`i` be the current position of `x`, and maintain:

> **Invariant I(i).** (a) (H) holds at every pair `(parent(j), j)` with `j != i`.
> (b) If `i` has a parent `p` and `i` has children, then `a[p] <= a[c]` for every
> child `c` of `i` — the *grandparent* bound survives even though the parent
> bound may not.

*Base.* `i = m` is a leaf, so (b) is vacuous and (a) is what we just argued.

*Step.* Let `p = parent(i)` and `w = a[p]`. If `w <= x` the excepted pair holds
too, so (H) holds everywhere; stop. Otherwise `w > x`; swap, so `a[p] = x`,
`a[i] = w`, and the position becomes `p`. Check I(p):

- pair `(p, i)`: `x < w`, holds;
- pair `(p, s)` for `i`'s sibling `s`: (H) held there before the swap, giving
  `w <= a[s]`, and `x < w`, so `x <= a[s]`;
- pair `(i, c)` for each child `c` of `i`: we now need `w <= a[c]`, which is
  exactly clause (b). **This is the step that fails without (b)**;
- every other pair is untouched.

So (a) holds for I(p), with `(parent(p), p)` the new exception. For (b): with
`g = parent(p)`, the children of `p` are `i` and `s`; `a[g] <= w = a[i]` because
(H) held at `(g, p)` before the swap, and `a[g] <= w <= a[s]`.

*Termination.* `p < i`, so the position strictly decreases and is bounded below
by 0. The loop ends at a stop or at `i = 0`, where there is no excepted pair, so
(H) holds. ∎ (push)

**Operation `pop()`: return `a[0]`, move the last element to index 0, shrink,
then sift down.** Shrinking preserves (S); the move can break (H) only at the
pairs `(0, c)`. Let `i` be the current position of the moved value `x`:

> **Invariant J(i).** (a) (H) holds at every pair except possibly `(i, c)` for
> `c` a child of `i`. (b) If `i` has a parent `p`, then `a[p] <= a[c]` for every
> child `c` of `i`.

*Base.* `i = 0` has no parent, so (b) is vacuous, and (a) is what the move left.

*Step.* If `i` has no children, (H) holds everywhere; stop. Otherwise let `m` be
the child with the **smaller** value, `v = a[m]`. If `x <= v` then `x <= a[c]`
for both children and (H) holds everywhere; stop. Otherwise swap, so `a[i] = v`,
`a[m] = x`, and the position becomes `m`. Check J(m):

- pair `(parent(i), i)`: now needs `a[parent(i)] <= v`, which is clause (b);
- pair `(i, o)` for the other child `o`: `v <= a[o]` because `m` was the smaller
  child — **the only place the word "smaller" is used, and the operation is
  wrong without it**;
- pair `(i, m)`: `v < x`, holds;
- pairs strictly inside `m`'s subtree are untouched.

For (b): the children of `m` satisfied `v = a[m] <= a[c]` before the swap by (H),
and `a[parent(m)] = a[i] = v`.

*Termination.* `m > i`, so the position strictly increases, bounded above by
`n-1`. By Claim A, the value returned was the minimum before the operation.
∎ (pop)

**Operation `heapify(a)`: for `i` from `n//2 - 1` down to `0`, sift down `i`.**

> **Invariant.** Before the iteration for index `i`, every index `j > i` roots a
> subtree satisfying (H).

*Base.* `i = n//2 - 1` is the last internal node, so every `j > i` is a leaf, and
a one-node subtree satisfies (H) vacuously.

*Step.* Both children of `i` exceed `i`, so they root valid heaps — the only
thing the sift-down argument needed. Applying it to the subtree at `i` restores
(H) throughout it, and indices outside that subtree are untouched.

*Termination.* `i` decreases by one each round; at `i = 0` the whole array
satisfies (H). ∎ (heapify)
:::

Now say plainly what the proof leaned on, because that list is where the bugs
live.

- **A total order that does not change.** Claim A used transitivity, and every
  step needed a consistent answer to `x <= y`. A comparator that is not a strict
  weak ordering — floats that may be `NaN`, a `key` with side effects — makes (H)
  unsatisfiable, and the heap returns the wrong element with no error.
- **Keys do not change while stored.** Mutate an object after pushing it and
  nothing re-establishes the invariant. Symptom: a pop that is not the minimum.
- **Only the ends are edited.** (S) held because we appended at index `n` and
  removed index `n-1`. `del a[i]` in the middle renumbers everything after `i`
  and destroys the tree: it is not a heap operation.
- **"Swap with the smaller child" is load-bearing.** Swap with the larger and the
  heap breaks immediately: from `[5, 1, 2]`, swapping 5 with 2 gives `[2, 1, 5]`,
  and `2 > 1`.
- **Nothing was proved about siblings, or about `a[-1]`.** One extra fact comes
  free: every internal node is `<=` one of its children, so the maximum of a
  min-heap is always a leaf, at an index `>= n//2`. A range, not a position.
- **Ties are unordered**, so heaps are not stable. When *Top Ten Trades by
  Notional Value* says "the trade that appears earlier in the input ranks first",
  that rule must be *in the key*.

<svg viewBox="0 0 760 300" role="img" aria-label="sifting down: swapping with the smaller child keeps the heap property, swapping with the larger child breaks it">
  <g>
    <circle class="fill" cx="80" cy="120" r="20"/>
    <text x="80" y="126" text-anchor="middle">5</text>
    <circle cx="40" cy="195" r="20"/>
    <text x="40" y="201" text-anchor="middle">1</text>
    <circle cx="120" cy="195" r="20"/>
    <text x="120" y="201" text-anchor="middle">2</text>
    <line x1="52" y1="178" x2="68" y2="138"/>
    <line x1="112" y1="178" x2="92" y2="138"/>
    <text x="80" y="245" text-anchor="middle">5 is too big here</text>
    <line x1="150" y1="105" x2="330" y2="70"/>
    <line x1="330" y1="70" x2="316" y2="66"/>
    <line x1="330" y1="70" x2="318" y2="78"/>
    <text x="215" y="80">swap with 1</text>
    <line x1="150" y1="150" x2="330" y2="205"/>
    <line x1="330" y1="205" x2="316" y2="197"/>
    <line x1="330" y1="205" x2="318" y2="209"/>
    <text x="215" y="200">swap with 2</text>
    <circle class="fill" cx="400" cy="45" r="20"/>
    <text x="400" y="51" text-anchor="middle">1</text>
    <circle cx="360" cy="115" r="20"/>
    <text x="360" y="121" text-anchor="middle">5</text>
    <circle cx="440" cy="115" r="20"/>
    <text x="440" y="121" text-anchor="middle">2</text>
    <line x1="372" y1="99" x2="388" y2="62"/>
    <line x1="428" y1="99" x2="412" y2="62"/>
    <text x="490" y="85">smaller child: still a heap</text>
    <circle class="fill" cx="400" cy="195" r="20"/>
    <text x="400" y="201" text-anchor="middle">2</text>
    <circle cx="360" cy="265" r="20"/>
    <text x="360" y="271" text-anchor="middle">1</text>
    <circle cx="440" cy="265" r="20"/>
    <text x="440" y="271" text-anchor="middle">5</text>
    <line x1="372" y1="249" x2="388" y2="212"/>
    <line x1="428" y1="249" x2="412" y2="212"/>
    <text x="490" y="235">larger child: 2 sits above 1</text>
  </g>
</svg>

## What it costs

Everything follows from the height of a complete binary tree.

**Height.** A complete tree of height `h` has levels `0..h-1` full, so it holds
at least `2^h` nodes: from `2^h <= n`, `h = floor(log2 n)`. The longest walk in
either direction is `h` steps.

**push**: at most `h` iterations, one comparison each, so `<= log2 n`. **pop**: at
most `h` iterations, two comparisons each — one to pick the smaller child, one to
test against it — so `<= 2 log2 n`. Both `O(log n)`, pop's constant twice push's.

**heapify, bottom-up.** Do not guess this one; count it. A node at height `j` can
fall at most `j` levels, and there are at most `ceil(n / 2^(j+1))` such nodes —
about `n/2` leaves at height 0, `n/4` parents at height 1, and so on. Total moves
are therefore at most

```
Σ_{j=0}^{h} (n / 2^(j+1)) · j  =  (n/2) · Σ_{j>=0} j / 2^j
```

and `Σ_{j>=0} j x^j = x/(1-x)^2`, which at `x = 1/2` is `2`. So the total is at
most `n`: heapify is **`Θ(n)`**, at under one move per element. (The exact count
is `n` minus the number of 1 bits in `n`.) The trace above did 3 moves for 6
elements, which is that bound working.

Building by `n` separate pushes has no such saving: the `i`-th push can walk
`floor(log2 i)` levels and on an adversarial input does, giving
`Σ_{i=1}^{n} log2 i = log2(n!) ≈ n log2 n − 1.44n` comparisons. **Heapify is
linear, repeated pushing is `n log n`**, and they build the same object.

**heapsort.** Heapify in `Θ(n)`, then pop `n` times at `O(log n)`: `Θ(n log n)`,
in place, `O(1)` extra memory. That is not slack to squeeze out — the pops alone
cost `Σ log i = log2(n!)`, and by the decision-tree bound no comparison sort
beats `log2(n!)` anyway ([[sorting]]).

**Bounded heaps.** A heap of size `k` fed `n` elements: `O(n log k)` time, `O(k)`
space. For *Top Ten Trades by Notional Value* that is `log2 10 ≈ 3.3` per element
against `log2(2·10^5) ≈ 17.6` for sorting everything, and memory drops from
200,000 records to ten. **Space** otherwise is nil: the heap *is* the array, and
both repairs are loops, so there is no recursion to blow.

**The cost people forget is the comparator.** All of the above counts
*comparisons*, and a comparison is `O(1)` only if the key is. Push
`(priority, timestamp, name)` and Python compares lexicographically: equal
priorities fall through to the timestamp, equal timestamps to the name, character
by character. Keys agreeing on the first field and differing only in an
`L`-character string cost `O(L log n)` per operation. A class with `__lt__` is
worse: every comparison is an interpreted function call.

## The implementation

```python run
import random


def sift_up(a, i):
    """Walk a[i] toward the root until its parent is no larger."""
    x = a[i]
    while i > 0:
        p = (i - 1) >> 1
        if a[p] <= x:
            break
        a[i] = a[p]                       # slide the parent down into the hole
        i = p
    a[i] = x


def sift_down(a, i, n=None):
    """Walk a[i] toward the leaves until both children are no smaller."""
    n = len(a) if n is None else n
    x = a[i]
    while True:
        c = 2 * i + 1
        if c >= n:
            break
        if c + 1 < n and a[c + 1] < a[c]:
            c += 1                        # descend into the SMALLER child
        if x <= a[c]:
            break
        a[i] = a[c]
        i = c
    a[i] = x


def heapify(a):
    for i in range(len(a) // 2 - 1, -1, -1):
        sift_down(a, i)


def push(a, x):
    a.append(x)
    sift_up(a, len(a) - 1)


def pop(a):
    last = a.pop()
    if not a:
        return last
    top, a[0] = a[0], last
    sift_down(a, 0)
    return top


def is_heap(a):
    return all(a[(i - 1) >> 1] <= a[i] for i in range(1, len(a)))


h = [5, 1, 8, 3, 2]
heapify(h)
print("heapified      ", h, "  min:", h[0], "  last cell:", h[-1], " max:", max(h))
assert is_heap(h) and h[0] == min(h) and h != sorted(h) and h[-1] != max(h)

rng = random.Random(7)
for _ in range(300):
    xs = [rng.randrange(-40, 40) for _ in range(rng.randrange(0, 25))]
    inc = []
    for x in xs:
        push(inc, x)
        assert is_heap(inc)
    assert [pop(inc) for _ in range(len(xs))] == sorted(xs)
    built = list(xs)
    heapify(built)
    assert is_heap(built) and (not xs or built[0] == min(xs))
print("300 random sequences: push/pop drains in sorted order, heapify holds (H)")
```

Three lines carry the weight.

`if c + 1 < n and a[c + 1] < a[c]: c += 1` is the entire reason `sift_down`
works, and the proof used it exactly once. Written this way it is one comparison,
not two: pick the smaller child, then compare `x` against it. The `c + 1 < n`
guard is the complete-tree boundary — the last internal node may have one child.

The pair `a[i] = a[p]` … `a[i] = x` is the **hole** technique. A textbook
`sift_up` swaps, writing both cells every step; this one writes the displaced
value into the hole and plants `x` once, at the end: same comparisons, half the
writes. It is also why `x` is read into a local first.

`sift_down(a, i, n=None)` takes an explicit length — useless for a priority queue
and essential for heapsort, where the array is a shrinking heap at the front and
a growing sorted region at the back. In real code use `heapq`: same algorithm,
in C.

## Variants you will meet

**Max-heap.** Python ships a min-heap only. Push `-x` and negate on the way out.
*Last Stone Weight* and *Remove Stones to Minimize the Total* are written so.

**Heapsort.** Build a *max*-heap in place, then repeatedly swap the root with the
last unsorted cell and sift down over a shrinking prefix. Ascending, in place,
`Θ(n log n)` worst case with no scratch buffer — the guarantee [[quicksort]] does
not give and [[merge-sort]] does not give for free. Its weaknesses, cache
behaviour and instability, are why library sorts keep it as introsort's fallback
arm.

```python run
CMPS = [0]


def sift_down_max(a, i, n):
    x = a[i]
    while True:
        c = 2 * i + 1
        if c >= n:
            break
        if c + 1 < n:
            CMPS[0] += 1
            if a[c + 1] > a[c]:
                c += 1
        CMPS[0] += 1
        if x >= a[c]:
            break
        a[i] = a[c]
        i = c
    a[i] = x


def heapsort(xs):
    a, n = list(xs), len(xs)
    for i in range(n // 2 - 1, -1, -1):          # linear build
        sift_down_max(a, i, n)
    build = CMPS[0]
    for end in range(n - 1, 0, -1):              # n-1 extractions
        a[0], a[end] = a[end], a[0]
        sift_down_max(a, 0, end)
    return a, build


def build_by_push(xs):
    a = []
    for x in xs:
        a.append(x)
        i = len(a) - 1
        while i > 0:
            p = (i - 1) >> 1
            CMPS[0] += 1
            if a[p] >= a[i]:
                break
            a[i], a[p] = a[p], a[i]
            i = p
    return a


print("%8s %12s %7s %14s %7s" % ("n", "heapify", "/n", "n pushes", "/n"))
for n in (1000, 4000, 16000):
    xs = list(range(n))                          # worst case for max-heap pushes
    CMPS[0] = 0
    _, build = heapsort(xs)
    CMPS[0] = 0
    build_by_push(xs)
    pushes = CMPS[0]
    print("%8d %12d %7.2f %14d %7.2f" % (n, build, build / n, pushes, pushes / n))
    assert build < 3 * n, "bottom-up heapify must stay linear"
    assert pushes > 4 * n, "repeated pushing must not"

import random
data = [random.Random(3).randrange(1000) for _ in range(400)]
CMPS[0] = 0
out, _ = heapsort(data)
assert out == sorted(data)
print("heapsort of 400 ints matches sorted(); comparisons =", CMPS[0],
      "~ n*log2(n) =", int(400 * 8.64))
```

The `/n` columns are the point: heapify's stays flat as `n` grows sixteenfold,
while the push column climbs with `log2 n`.

**Bounded heap for the k best.** Keep a min-heap of size `k`; evict the root
whenever a larger element arrives. `O(n log k)` time, `O(k)` space, and it works
on a stream you cannot store. Chapter: [[top-k]]; problems: *Top-K Using a
Priority Queue*, *Top Ten Trades by Notional Value*, *Fixed-K Kth Largest
Stream*.

**Two heaps facing each other.** A max-heap of the smaller half and a min-heap of
the larger half, balanced, gives the running median in `O(log n)`:
[[median-maintenance]]. A different pairing — jobs by arrival time, available
jobs by cost — is the skeleton of *Single-Threaded CPU* and *Assign Tasks to
Servers*.

**k-way merge.** One head per sorted stream, keyed by value plus stream id; pop,
emit, push that stream's next element. `O(N log k)`: [[k-way-merge]].

**Best-first search.** The frontier of [[dijkstra]] and A* is a heap keyed by
tentative distance; the same structure drives Prim's [[minimum-spanning-tree]].

**Sweep with a heap.** Sort events by start; hold the *ends* of the active
intervals in a min-heap; pop everything that ended before the next start. The
heap's size is the number of simultaneous intervals — the answer to *Meeting
Rooms II*. See [[intervals]] and [[scheduling]].

**Lazy deletion.** A heap cannot remove an arbitrary element, so do not try: push
a new entry instead of updating an old one, and discard stale entries as they
surface at the root. Every operation stays `O(log n)`, and this is why Dijkstra
with a binary heap is written with duplicate pushes and an
`if d > dist[u]: continue` guard. The alternative — an **indexed heap**, with a
`position[item]` map updated by every swap — is what "decrease-key" means.

**d-ary heaps.** Each node gets `d` children: height `log_d n`, cheaper pushes,
dearer pops (`d` comparisons per level), happier cache.

**When a heap is overkill.** Small bounded integer keys: buckets are `O(1)` with
no comparisons ([[counting-sort]]). One selection from a static array:
[[quickselect]], expected `O(n)`.

## Recognising it in a statement

Ordered by how much you should trust them.

1. **"Repeatedly take the largest/smallest, then put something back."** A loop
   whose body both removes an extreme and inserts a new value is the signature;
   there is no sorted order to maintain because the set changes every round.
   *Last Stone Weight*, *Connect N Ropes With Minimum Cost*, *Remove Stones to
   Minimize the Total*.
2. **A stated complexity of `O(n log k)` or memory bound of `O(k)`.** *Top-K
   Using a Priority Queue* says "An `O(n log k)` solution is expected"; *Top Ten
   Trades by Notional Value* says "Use a heap that retains at most ten
   candidates". When the problem names the complexity, it has named the
   structure.
3. **"The next one to become free", "the least loaded", "the earliest
   deadline"** — a superlative over a set being mutated as you go: *Assign
   Partitions to the Least-Loaded Servers*, *Single-Threaded CPU*.
4. **"Maximum number of simultaneous X"** — rooms, chairs, machines. Sweep with
   a heap of end times; the answer is its peak size. *Minimum Number of Chairs*.
5. **A stream, or "after each event report …"**: you cannot re-sort per event,
   and may not be able to store the input ([[streaming]]).
6. **Several sorted inputs, one sorted output.** *Merge Three Sorted Arrays*.
7. **An explicit tie-breaking rule inside a traversal.** *Topological Sort with
   Secondary Ordering* — a queue is correct but not deterministic.

The anti-signals:

- **The set never changes and you get one question.** Sort, or [[quickselect]].
- **"How many are less than x", "the element of rank r", "the next value above
  x".** A heap answers none of these: [[ordered-set]], [[fenwick-tree]], or a
  sorted array with [[binary-search]].
- **"Remove this particular element."** No such operation; you are choosing
  between lazy deletion and a different structure, and should say so out loud.
- **A sliding window maximum.** A monotonic deque is `O(n)`: [[monotonic-stack]].
- **"Sorted output" alone.** A heap does not hand you sorted data; draining one
  does, and that is heapsort, which `sorted()` beats.

## Traps

**Wrong polarity for top-k.** For the `k` *largest* you keep a **min**-heap, so
the root is the weakest survivor and is what you evict. It feels backwards and is
the single most common heap bug. Symptom: the answer is the `k` smallest, and
tests where `k` equals `n` still pass. Related: forgetting to negate back.

**Non-comparable payloads behind the key.** `(priority, some_dict)` works until
two priorities tie, at which point Python compares the dicts and raises
`TypeError`. Symptom: a crash on *some* inputs, never the samples. Fix: a unique
comparable tiebreaker between the key and the payload.

**Reading `heap[-1]` as the maximum, or slicing the array as if sorted.** Only
`heap[0]` is meaningful. Symptom: correct on inputs of size 1 to 3, wrong beyond.

**Mutating a key already in the heap**, or `del heap[i]` / `heap.remove(x)`. The
first breaks (H) with nothing to restore it; the others renumber the array and
shred the tree. Symptom: silently wrong answers, no exception.

**Pushing everything, then popping `k`.** `O(n log n)` time and `O(n)` memory
when the statement asked for `O(n log k)` and `O(k)`. Symptom: passes, then times
out or runs out of memory — what *Top Ten Trades by Notional Value* is testing
with its 200,000-row bound.

**Popping an empty heap.** Guard with `if heap:` before every peek; in a
simulation loop this fires at the very last iteration.

**Using `<=` where the statement says `<`.** *Insert into a Min-Heap* returns the
array itself, so an equal-value swap yields a valid heap with the wrong layout.
Symptom: your heap-property checker passes and the grader does not.

```python run
import heapq

nums = [7, 2, 9, 4, 9, 1, 8]
k = 3


def top_k_right(nums, k):
    h = []                                   # MIN-heap holding the k largest
    for x in nums:
        if len(h) < k:
            heapq.heappush(h, x)
        elif x > h[0]:
            heapq.heapreplace(h, x)          # one sift_down, not a pop plus a push
    return sorted(h, reverse=True)


def top_k_wrong(nums, k):
    h = []                                   # MAX-heap, capped at k
    for x in nums:
        heapq.heappush(h, -x)
        if len(h) > k:
            heapq.heappop(h)                 # evicts the LARGEST seen so far
    return sorted((-v for v in h), reverse=True)


print("nums                         ", nums)
print("k largest, min-heap of size k:", top_k_right(nums, k))
print("k largest, max-heap of size k:", top_k_wrong(nums, k), "<- the k smallest")
assert top_k_right(nums, k) == [9, 9, 8]
assert top_k_wrong(nums, k) == [4, 2, 1]

h = [5, 1, 8, 3, 2]
heapq.heapify(h)
print("heapified                    ", h, " h[-1] =", h[-1], " max =", max(h))
assert h[0] == min(h) and h != sorted(h)

tasks = [(2, {"id": "a"}), (2, {"id": "c"}), (1, {"id": "b"})]
try:
    bad = []
    for pr, payload in tasks:
        heapq.heappush(bad, (pr, payload))
    print("no error raised")
except TypeError as e:
    print("pushing (priority, dict):     TypeError:", e)

good = []
for seq, (pr, payload) in enumerate(tasks):
    heapq.heappush(good, (pr, seq, payload))   # seq is unique: ties stop here
order = [heapq.heappop(good)[2]["id"] for _ in range(len(good))]
print("with a sequence tiebreak:     ", order)
assert order == ["b", "a", "c"]
```

## What to memorise

Four lines of arithmetic and one sentence.

```python
parent(i) = (i - 1) // 2      left(i) = 2i + 1      right(i) = 2i + 2
push:    append, then walk up while smaller than the parent
pop:     take a[0], move the last cell to 0, walk down into the smaller child
heapify: sift_down every index from n//2 - 1 back to 0
```

**The sentence** that turns a problem into a heap: *"Do I keep needing the
extreme of a set that keeps changing?"* If the set is static, sort. If the
question is about rank rather than extremes, it is not a heap at all.

**The habit**: make every heap entry a tuple that is exactly the ordering rule,
read left to right, ending in something unique. `(-notional, arrival_index, id)`
says "largest notional first, ties to whoever came first" and cannot fall through
into a payload. Decide the polarity by asking *what do I want to throw away*, and
put that at the root.

Numbers worth carrying: `log2(10^5) ≈ 17`, `log2(10^6) ≈ 20`, `log2(10) ≈ 3.3`.
Heapify is `Θ(n)`, push and pop are `O(log n)`, heapsort is `Θ(n log n)` in
place, a size-`k` heap over `n` items is `O(n log k)` and `O(k)` space. A pop
costs about twice a push.

## Check yourself

:::check
Building a heap by `n` pushes costs `Θ(n log n)`, but sifting down every internal
index costs `Θ(n)`. Both produce a valid heap over the same elements. Why is one
linear and the other not?
--
Because the two methods spend their budget on different halves of the tree.

A push starts at a leaf and may walk to the root, so its cost is the node's
*depth*, and most nodes are deep — half are leaves at depth `log2 n`. Total:
`Σ_i log2 i = log2(n!) = Θ(n log n)`.

A sift-down starts at a node and may walk to a leaf, so its cost is the node's
*height*, and most nodes are short — half are leaves of height 0 and cost
nothing, a quarter have height 1, only the root has height `log2 n`. Total:
`Σ_j (n / 2^(j+1)) · j = (n/2) · Σ_j j/2^j = n`.

The distributions are mirror images and the series converges in one direction
only. The catch: this helps only when you already hold all `n` elements. A heap
fed by a stream has no choice but to push.
:::

:::check
Someone says: "a heap's array is sorted enough — `heap[0]` is the minimum, so
`heap[-1]` must be the maximum, and `heap[:k]` gives me the k smallest." Where
are they wrong, and what *can* you say about where the maximum is?
--
All three are wrong, the first two for the same reason: the invariant constrains
only parent-child pairs. `[1, 2, 8, 5, 3]` is a valid min-heap whose last cell
holds 3, whose index 2 holds the maximum, and whose first three cells are not the
three smallest (those are 1, 2, 3).

What you *can* say: every internal node is `<=` at least one of its children, so
it is never a strict maximum. The maximum of a min-heap is therefore a leaf, at
some index in `n//2 .. n-1` — a range of `n/2` candidates, not a position. To get
the `k` smallest, pop `k` times, at `O(k log n)`.
:::

:::check
To return the `k` largest elements of a long stream you keep a heap of size `k`.
Should it be a min-heap or a max-heap, and why does the other one give the wrong
answer rather than merely being slower?
--
A **min**-heap. It holds the `k` best candidates so far, and when a new element
arrives you evict the *weakest* — the smallest — so the smallest has to be the
one you can reach, at the root.

A max-heap capped at `k` evicts its root, the largest, so it throws away exactly
what you were trying to keep and ends up holding the `k` smallest. A wrong
answer, not a slow one.

The rule generalises: **the root is what you are prepared to discard.** *Top-K
Using a Priority Queue* and *Top Ten Trades by Notional Value* are both this
pattern; the latter pins `k = 10`, so the heap is `O(10)` memory over 200,000
rows.
:::

:::check
In `sift_down`, why must you compare the two children with each other before
comparing either with the sifting value? Give a concrete three-element
counterexample for the version that just swaps with the left child when it is
smaller.
--
Because after the swap the value you moved up sits above *both* children, so it
must be `<=` both — and only the smaller child gives that for free.

Take `[5, 1, 2]`: root 5, children 1 and 2. Swapping with the *larger* child
gives `[2, 1, 5]`, and now `a[0] = 2 > a[1] = 1`: (H) is broken at the pair
`(0, 1)`, which the operation was not even looking at. Swapping with the smaller
child gives `[1, 5, 2]`, a valid heap.

In the proof this is the line checking the pair `(i, o)`. It is the only place in
the entire argument where the word *smaller* is used, so it is the one line you
cannot paraphrase away.
:::

:::check
*Meeting Rooms II* asks for the minimum number of rooms needed for a set of
meetings. Describe the heap solution, say exactly what the heap stores, and
explain why the heap's size is the answer.
--
Sort by start time. Keep a min-heap of the **end times of the meetings currently
in progress**. For each meeting in start order: pop every end time `<=` this
start (those rooms are now free), then push this meeting's end time. The answer
is the largest size the heap ever reaches.

That size is the number of meetings started and not finished — the rooms in use
at that instant. Its maximum is a lower bound (those meetings are pairwise
simultaneous, so they need distinct rooms) and is achievable (the algorithm
reuses a room whenever one is free).

A min-heap, because the only end time that can possibly be free by the next start
is the earliest, and that set changes at every step. Cost: `O(n log n)` for the
sort, then `n` pushes and at most `n` pops. *Minimum Number of Chairs* is the
same sweep with a different noun.
:::

