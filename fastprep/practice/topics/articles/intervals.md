# Interval Problems

> An interval problem is never really about intervals. It is about endpoints on a
> line, and about the single number you have to remember once you have agreed to
> visit those endpoints in order.

## When you reach for it

The input is a pile of pairs, and each pair is a *range*: a meeting from 9 to 10,
a process alive from `start` to `end`, a block of card numbers from `lo` to `hi`.
The question is then one of four — do they overlap, how much of the line do they
cover together, how many are alive at once, or which subset can you keep without
conflict.

That family is huge here: 182 problems in this bank use it, #23 of 150. Almost
every one is one of these shapes:

- **Collapse the union** — *Merge Intervals*, which a dozen companies here ask
  verbatim, and *Compress Consecutive Integer Ranges*.
- **Measure the union** — *Process Execution Time* wants the total time at least
  one process is running; *Dasher Active Time* is the same sum with a different
  noun.
- **Count what is simultaneous** — *Meeting Rooms II*, *Get Minimum Cores*,
  *Minimum Number of Chairs*. All one question: what is the largest number of
  intervals covering a single point?
- **Intersect two schedules** — *Interval List Intersections*, *Find First Common
  Availability*.
- **Choose a conflict-free subset** — *Minimum Removals for Non-Overlapping
  Intervals*, *Maximum Number of Events That Can Be Attended*.
- **Maintain a calendar online** — *My Calendar I*, *In-Memory Meeting Room
  Manager*: intervals arrive one at a time, each accepted or rejected against
  everything booked so far.

The trigger is structural, not lexical: pairs `(s, e)` with `s <= e` from a
totally ordered universe, and an answer depending on how they sit relative to
each other on that one axis. Time is the usual axis, but *Card Range Obfuscation
Part1* ranges over card numbers and *Memory Allocator* over addresses.

It is the wrong tool in three situations. If the pairs are **edges**, not ranges —
`(u, v)` meaning "u knows v" — you want [[union-find]] or [[graphs]]; nothing
about `u < v` means anything. If you must answer **many queries against a static
set** — *Closed Interval Overlap Queries*, *Schedule Tasks with an Interval Tree*
— one sweep is not enough and you want an interval tree or a [[segment-tree]].
And if the intervals carry **weights** and you want the heaviest conflict-free
subset — *Max Sum of Non-Overlapping Intervals* — the greedy in this chapter is
simply wrong, and you need [[dynamic-programming|DP with a binary search]].

## The idea

Sorting turns a two-dimensional pile into a one-dimensional walk.

An interval is a point in the plane: `(start, end)`. A set of `n` intervals is a
scatter of `n` points, and "do any two overlap" is a question about `n(n-1)/2`
pairs — the shape that makes people write a double loop. Sort by start and the
pile becomes a line you read left to right, and the entire past collapses into
**one number**.

Here is the precise claim, and it is the whole chapter. Walk the intervals in
order of start. Suppose you are holding a *current block* `[cs, ce]`, the union of
a run of intervals that have all touched each other. The next interval `[s, e]`
has `s >= cs`, because the list is sorted. So exactly one of two things is true:

- `s <= ce`: the new interval begins before the block ends, so the block and it
  overlap, and their union is the single interval `[cs, max(ce, e)]`.
- `s > ce`: it begins after the block ends. And now the useful half — every
  *remaining* interval also starts at or after `s`, so no future interval can
  reach back and touch this block either. The block is finished. Emit it and
  start a new one at `[s, e]`.

Nothing about the intervals inside the block survives except `ce` — not how many
there were, not where they started. One integer summarises an arbitrarily long
prefix, which is why the scan needs O(1) memory per step and no inner loop.

<svg viewBox="0 0 660 230" role="img" aria-label="intervals drawn as bars sorted by start, with a moving wall at the current block end">
  <g>
    <line x1="30" y1="200" x2="640" y2="200"/>
    <text x="30" y="220">1</text>
    <text x="130" y="220">4</text>
    <text x="230" y="220">6</text>
    <text x="330" y="220">9</text>
    <text x="410" y="220">11</text>
    <text x="530" y="220">13</text>
    <text x="610" y="220">15</text>
    <rect class="fill" x="30" y="30" width="100" height="18" rx="4"/>
    <text x="140" y="44">[1,4]</text>
    <rect class="fill" x="70" y="60" width="40" height="18" rx="4"/>
    <text x="140" y="74">[2,3] nested: ce stays 4</text>
    <rect class="fill" x="230" y="90" width="100" height="18" rx="4"/>
    <text x="340" y="104">[6,9]</text>
    <rect class="fill" x="310" y="120" width="100" height="18" rx="4"/>
    <text x="420" y="134">[8,11] extends ce to 11</text>
    <rect class="fill" x="530" y="150" width="80" height="18" rx="4"/>
    <text x="440" y="164">[13,15] starts past 11: flush</text>
    <line x1="130" y1="20" x2="130" y2="200"/>
    <line x1="410" y1="20" x2="410" y2="200"/>
    <text x="150" y="18">a wall at ce; nothing later can reach back over it</text>
  </g>
</svg>

There is a second way to look at the same picture, and it is worth holding both.
Forget the intervals as objects; keep only their endpoints, each tagged `+1`
where an interval opens and `-1` where it closes. Sort the tags by position and
keep a running total: that total is how many intervals cover the point you are
standing on. Its maximum is the peak concurrency, and the maximal stretches where
it is positive are precisely the merged blocks. One sorted walk, two questions.
The general form has its own chapter: [[sweep-line]].

## Worked by hand

Take `[[1, 4], [6, 9], [2, 3], [8, 11], [13, 15]]`, closed intervals over the
integers. Sorted by start: `[1,4], [2,3], [6,9], [8,11], [13,15]`.

`out` is the finished blocks, `(cs, ce)` the block in hand.

| step | interval | block before | `s <= ce`? | action | block after | `out` |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [1,4] | — | — | open the first block | (1, 4) | — |
| 2 | [2,3] | (1, 4) | 2 <= 4, yes | `ce = max(4, 3) = 4` | (1, 4) | — |
| 3 | [6,9] | (1, 4) | 6 <= 4, no | flush, open | (6, 9) | [1,4] |
| 4 | [8,11] | (6, 9) | 8 <= 9, yes | `ce = max(9, 11) = 11` | (6, 11) | [1,4] |
| 5 | [13,15] | (6, 11) | 13 <= 11, no | flush, open | (13, 15) | [1,4], [6,11] |
| — | end | (13, 15) | — | flush | — | [1,4], [6,11], [13,15] |

Total covered time, counting inclusively as *Process Execution Time* asks you to:
`(4-1+1) + (11-6+1) + (15-13+1) = 4 + 6 + 3 = 13`.

Now the same five intervals through the second lens. Each closed interval
`[s, e]` over the integers is the half-open `[s, e+1)`, so it contributes `+1` at
`s` and `-1` at `e + 1`.

| position | tag | running count | note |
| --- | --- | --- | --- |
| 1 | +1 | 1 | [1,4] opens |
| 2 | +1 | 2 | [2,3] opens — two alive |
| 4 | -1 | 1 | [2,3] closed after 3 |
| 5 | -1 | 0 | [1,4] closed after 4 → block ends |
| 6 | +1 | 1 | [6,9] opens |
| 8 | +1 | 2 | [8,11] opens |
| 10 | -1 | 1 | [6,9] closed after 9 |
| 12 | -1 | 0 | [8,11] closed after 11 → block ends |
| 13 | +1 | 1 | [13,15] opens |
| 16 | -1 | 0 | done |

Peak count 2, so two meeting rooms. Four things in these two tables are worth a
second look, and none of them is visible in the code.

**Step 2 is the reason the `max` is there.** `[2,3]` is entirely inside the
block. If the update were `ce = e` rather than `ce = max(ce, e)`, the block would
*shrink* to `[1,3]` and the point 4 would silently drop out of the answer. The
sorted order guarantees the new start is not smaller; it says nothing at all
about the new end.

**Step 3 finished a block on a single comparison.** We never looked at `[8,11]`
or `[13,15]` before declaring `[1,4]` complete, and did not have to: sortedness
says every unseen start is at least 6. This one-sided guarantee is what sorting
buys, and the proof below is mostly ceremony around it.

**The zeros in the second table sit exactly at the gaps in the first.** The
counter returns to 0 after positions 5 and 12, and the merged blocks are `[1,4]`,
`[6,11]`, `[13,15]`. Merging is "the maximal runs where the counter is positive";
concurrency is "the maximum it reaches". Which is why *Process Execution Time*
and *Meeting Rooms II* feel like different problems and are not.

**The close tags sit at `e + 1`, not `e`.** With integer closed intervals, an
interval that ends at 4 is still running *during* 4. Putting the `-1` at 4 would
report 1 room for two meetings that genuinely both occupy minute 4. Almost every
wrong answer on this topic is a variant of that sentence.

## Why it is correct

Two claims deserve proofs. The first is that the one-pass merge really computes
the union. The second is the theorem that makes *Meeting Rooms II* a three-line
problem: the minimum number of rooms equals the maximum overlap.

:::proof The sorted scan computes the union exactly
**Setup.** Intervals `I₁, …, I_n`, each `I_k = [s_k, e_k]` with `s_k <= e_k`,
indexed so that `s_1 <= s_2 <= … <= s_n`. Write `U_k = I_1 ∪ … ∪ I_k` for the
union of the first `k` as a set of points. A finite union of closed intervals
decomposes uniquely into **maximal** closed intervals — its connected components,
pairwise disjoint and separated by non-empty gaps. Call it `comp(U_k)`.

**Invariant.** After the loop has consumed `I_1 … I_k` (so `k >= 1`), let `out`
be the emitted list and `(cs, ce)` the block in hand. Then:

- **(I1)** `out ++ [(cs, ce)]` equals `comp(U_k)`, in increasing order;
- **(I2)** `cs <= s_k` and `ce = max(e_1, …, e_k restricted to the last
  component)`; in particular `ce` is the right endpoint of the last component;
- **(I3)** every interval in `out` has its right endpoint strictly less than
  `cs`.

**Base case.** `k = 1`. `out` is empty and `(cs, ce) = (s_1, e_1)`. The union of
one interval has one component, namely itself, so (I1) holds; (I2) holds with
equality; (I3) is vacuous.

**Inductive step.** Assume the invariant after `k` and consume
`I_{k+1} = [s, e]`. By the sort, `s = s_{k+1} >= s_k >= cs`.

*Case A: `s <= ce`.* Then `s ∈ [cs, ce]`, so `[s, e]` and `[cs, ce]` intersect,
and the union of two intersecting closed intervals is the single closed interval
`[min(cs, s), max(ce, e)] = [cs, max(ce, e)]`. It cannot also touch an interval
of `out`: by (I3) each of those ends strictly before `cs`, and `[s, e]` ⊆
`[cs, ∞)`. So `comp(U_{k+1})` is `out` unchanged plus the one component
`[cs, max(ce, e)]`. The code sets `ce ← max(ce, e)` and nothing else, restoring
(I1) and (I2); `out` and `cs` do not move, so (I3) survives.

*Case B: `s > ce`.* Then `[s, e]` is disjoint from `[cs, ce]` and, by (I3), from
everything in `out`, and the gap `(ce, s)` is non-empty. So
`comp(U_{k+1}) = comp(U_k) ++ [[s, e]]`. The code appends `(cs, ce)` to `out` and
sets `(cs, ce) ← (s, e)`, which is exactly that list, splitting it after the last
old component: (I1) holds. (I2) holds because the new last component is `[s, e]`
itself. (I3) holds because the newly appended element of `out` ends at `ce < s =
cs`, and all earlier ones end before the old `cs <= ce`.

**Termination.** The loop body runs once per interval and does O(1) work with no
nested loop, so it performs exactly `n` iterations and stops. The final flush
appends the last block.

**Conclusion.** After `n` iterations and the flush, the output is `comp(U_n)`:
the maximal, pairwise disjoint, increasing intervals whose union is exactly the
union of the input. Maximality is (I3) read forwards — consecutive outputs are
separated by a non-empty gap, so no two of them could have been merged. ∎
:::

:::proof Minimum rooms = maximum overlap
**Setup.** `n` meetings, meeting `k` occupying the half-open interval
`[s_k, e_k)`. A *schedule* assigns each meeting a room so that two meetings in
the same room never share a point. Let `R` be the fewest rooms for which a
schedule exists, and let `M = max_x |{k : x ∈ [s_k, e_k)}|` be the largest number
of meetings covering any single instant.

**`R >= M`.** Let `x` be an instant covered by `M` meetings. Those `M` meetings
pairwise share the point `x`, so no two may go in the same room: any schedule
uses at least `M` distinct rooms.

**`R <= M`.** Process the meetings in increasing order of start, assigning each
to any room free at its start instant. Suppose meeting `k`, starting at `x`,
finds `r` rooms busy. Each of those `r` rooms holds a meeting `j` placed earlier,
so `s_j <= x`, and still running, so `e_j > x`; each therefore covers `x`. With
meeting `k`, which also covers `x`, that is `r + 1` meetings at one instant, so
`r + 1 <= M` and a room numbered at most `M` is free. By induction on the
processing order the greedy finishes inside `M` rooms and never double-books.

**Conclusion.** `R = M`, and `M` is computable by the sweep: sort the `2n`
endpoints, add `+1` at each start and `-1` at each end, and take the running
maximum. ∎
:::

Both arguments leaned on assumptions, and that list is where the bugs live.

- **The input is sorted by start, ascending.** Used twice in the first proof: to
  know `s >= cs` (Case A) and to know no future interval can reopen a flushed
  block (Case B). Sorting by end breaks both.
- **Intervals are well formed: `s <= e`.** A backwards interval is empty, and
  Case A's union argument quietly fails. Normalise at the door.
- **The overlap test matches the convention.** The proof used `s <= ce` because
  intervals are closed and touching at a point counts as intersecting. For
  half-open `[s, e)` intervals, touching does *not* count, and the test must be
  `s < ce`. Getting this backwards changes the answer by exactly one room, or
  merges two blocks that should be separate.
- **`ce` is the maximum end so far in the block, not the last one.** (I2) is
  the load-bearing part of the invariant, and the only thing standing between you
  and nested intervals.
- **Rooms are interchangeable.** The second proof assigned meeting `k` to *any*
  free room. *Minimum Meeting Rooms with Assignments*, where a meeting may only
  use certain rooms, is not this theorem; the equality can fail and it becomes a
  matching problem.
- **Endpoints are exactly comparable.** Floats parsed from "09:30", or two time
  zones mixed in one list, break the total order the sort assumes.

## What it costs

Split the work in two: arranging the endpoints, then walking them.

**The walk is linear.** The merge loop runs once per interval and does a constant
number of comparisons plus one amortised `append` — no nested loop, because the
prefix is summarised by `ce`. That is `Θ(n)` after the sort, and the sweep over
`2n` tagged endpoints is likewise `Θ(n)`. The two-pointer intersection of sorted
lists of lengths `n` and `m` advances one pointer per iteration and neither ever
goes backwards, so it runs at most `n + m` times — an [[amortized-analysis|
amortised]] counting argument, not a bound you can read off the code.

**The sort dominates:** `Θ(n log n)` comparisons, so the whole thing is
`Θ(n log n)` time. Space is `Θ(n)` for the sorted copy and the output, plus
`O(1)` working state — although in Python `sorted()` allocates a new list, and the
output of a merge can be as large as the input when nothing overlaps.

Is the `log` avoidable? In the comparison model, no, and the reduction is worth
knowing. Given `n` numbers `x_1 … x_n`, build the degenerate intervals
`[x_i, x_i]`; merging them yields the distinct values in increasing order with
`Θ(n)` extra work. A merge running in `o(n log n)` comparisons would therefore
sort in `o(n log n)` comparisons, contradicting the `Ω(n log n)` sorting bound.
Interval merging is *exactly* as hard as sorting, and the only escape is to leave
the comparison model: with small integer coordinates a difference array
([[prefix-sums]]) or a [[counting-sort]] gives `Θ(n + M)` for coordinate range
`M`. *Minimum Number of Chairs* over a day of minutes is that case; *Merge
Intervals* with endpoints up to `10⁹` is not.

Three costs people forget:

- **The heap variant is not free.** The popular *Meeting Rooms II* solution
  keeps a min-heap of end times: `n` pushes and up to `n` pops at `O(log n)`, so
  the same `O(n log n)` class as the sweep, but with a heap's constant factor and
  `O(n)` extra memory, for the number two sorted endpoint arrays already give.
  Use it when you need *which* room, not how many ([[heap]]).
- **Comparisons are not always unit cost.** A `key=lambda` costs a call per
  element, and intervals carrying labels (*Merge Intervals with Names*) may end
  up comparing strings. See [[custom-comparators]].
- **The output can be the bottleneck.** *Insert Interval* cannot beat `O(n)`
  even though binary search finds the insertion point in `O(log n)`: the
  untouched suffix still has to be copied into the result.

## The implementation

Merge, coverage and peak overlap, with the claims checked against a brute-force
count that marks every integer point.

```python run
import random


def merge(intervals):
    """Union of CLOSED integer intervals, as sorted maximal blocks."""
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)    # nested interval must not shrink it
        else:
            out.append([s, e])                 # a fresh row: never alias the input
    return out


def covered(intervals):
    """Total time at least one interval is running (inclusive units)."""
    return sum(e - s + 1 for s, e in merge(intervals))


def max_overlap(intervals):
    """Peak number of intervals covering one point = rooms needed."""
    events = []
    for s, e in intervals:
        events.append((s, 1))
        events.append((e + 1, -1))     # closed -> half-open; ties then sort themselves
    events.sort()
    cur = best = 0
    for _, delta in events:
        cur += delta
        best = max(best, cur)
    return best


demo = [[1, 4], [6, 9], [2, 3], [8, 11], [13, 15]]
print("input   ", demo)
print("merged  ", merge(demo))
print("covered ", covered(demo), "units;   rooms needed:", max_overlap(demo))
assert merge(demo) == [[1, 4], [6, 11], [13, 15]]
assert covered(demo) == 13 and max_overlap(demo) == 2


def brute_covered(iv):
    pts = set()
    for s, e in iv:
        pts.update(range(s, e + 1))
    return len(pts)


def brute_overlap(iv):
    if not iv:
        return 0
    lo, hi = min(s for s, _ in iv), max(e for _, e in iv)
    return max(sum(1 for s, e in iv if s <= t <= e) for t in range(lo, hi + 1))


rng = random.Random(4)
for _ in range(500):
    iv = [[s, s + rng.randint(0, 5)]
          for s in (rng.randint(0, 14) for _ in range(rng.randint(0, 8)))]
    blocks = merge(iv)
    assert all(blocks[i][1] < blocks[i + 1][0] for i in range(len(blocks) - 1)), iv
    assert covered(iv) == brute_covered(iv), iv
    assert max_overlap(iv) == brute_overlap(iv), iv
print("500 random instances: blocks disjoint, coverage and peak match a point count")
```

Three lines carry the weight.

`for s, e in sorted(intervals)` is the whole algorithm's premise, and it is one
call. Everything after it is allowed to be simple *because* of it. If you ever
find yourself writing an inner loop over `out`, you have lost the invariant — go
back and check the sort.

`out[-1][1] = max(out[-1][1], e)` is invariant (I2) written down. The `max` looks
defensive and is not: the sort orders starts and leaves ends arbitrary, so a
later interval genuinely can end earlier.

`events.append((e + 1, -1))` does two jobs. It converts the closed interval to
the half-open `[s, e+1)`, so a meeting ending at 4 still occupies 4; and because
closes now land strictly past the last instant they cover, ties between a close
and an open resolve themselves. With continuous coordinates you cannot add 1, and
must instead sort `(t, delta)` so `-1` precedes `+1` at equal `t` — which tuple
order gives free, since `-1 < 1`. Both express one sentence: *a meeting that ends
when another begins does not need a second room.*

## Variants you will meet

**Merge with adjacency.** *Compress Consecutive Integer Ranges* and *Compact the
List* treat `[1,3]` and `[4,6]` as one run, since 3 and 4 are adjacent integers:
the test becomes `s <= ce + 1`.

**Total covered length.** *Process Execution Time*, *Dasher Active Time*: merge,
then sum with the inclusive `e - s + 1`.

**Peak concurrency and minimum resources.** *Meeting Rooms II*, *Get Minimum
Cores*, *Minimum Number of Chairs*: the second proof above. Sweep tagged
endpoints, or sort starts and ends into two arrays and merge them with two
pointers ([[two-pointers]]), or keep a min-heap of end times ([[heap]]) — the
heap is the only one that can also say *which* room.

**Insert one interval.** *Insert Interval*: given a sorted disjoint list, splice
in `[s, e]` in three phases — copy everything ending before `s`, absorb
everything overlapping into `[min(starts), max(ends)]`, copy the rest.

**Intersect two sorted lists.** *Interval List Intersections*, *Find First
Common Availability*: the intersection of `[a1,a2]` and `[b1,b2]` is
`[max(a1,b1), min(a2,b2)]`, non-empty iff `max(a1,b1) <= min(a2,b2)`. Emit it if
non-empty, then advance the pointer whose interval ends first — it can meet
nothing later. *Combine Two Vectors of Intervals* is the union version of the
same walk.

**Complement and gaps.** *Generate Available Time Slots*, *Build a Combined
People Schedule*: merge the busy intervals, then emit the gap between each
consecutive pair — plus the slivers before the first block and after the last,
which is where this one is always wrong first.

**Maximum conflict-free subset.** *Minimum Removals for Non-Overlapping
Intervals*, *Maximum Number of Events That Can Be Attended*: sort by **end** and
take greedily. Note the swap — the union wants starts, a subset wants ends. The
wider family is [[scheduling]].

**Weighted selection.** *Max Sum of Non-Overlapping Intervals*: the greedy dies,
because one heavy long interval can beat many light short ones. Sort by end and
let `best[i]` be the best total over the first `i`; then
`best[i] = max(best[i-1], w_i + best[p(i)])`, with `p(i)` the last interval
ending before `i` starts, found by [[binary-search]]. [[dynamic-programming]] in
interval clothing.

**Online conflict checking.** *In-Memory Meeting Room Manager*, *My Calendar I*:
keep the bookings sorted by start and, per candidate, binary-search the
predecessor and check two neighbours — `O(log n)` for both find and insert if the
container is a balanced tree or [[ordered-set]].

**Circular intervals.** *Minimum Servers for Cyclic Daily Tasks*: a task from
22:00 to 02:00 wraps. Split every wrapping interval in two, or sweep two copies
of the timeline. Never compare endpoints modulo anything.

**Many intervals, many queries.** *Closed Interval Overlap Queries*, *Batch
Point-in-Range Queries*: sort the queries in with the intervals and answer them
in one combined sweep, or build a [[segment-tree]] / [[fenwick-tree]] over
compressed coordinates.

**More than one axis.** Rectangles, skylines and area unions are intervals in one
axis swept along the other: [[sweep-line]]. *Union of K Sorted Interval Streams*
is the merge above fed by a [[k-way-merge]].

Here is the greedy variant, with the wrong rule next to it and a brute-force
check that the right one is actually optimal.

```python run
from itertools import combinations
import random


def max_disjoint_by_end(iv):
    """Largest set of pairwise disjoint closed intervals. Sort by END."""
    taken, last_end = 0, float("-inf")
    for s, e in sorted(iv, key=lambda p: p[1]):
        if s > last_end:
            taken += 1
            last_end = e
    return taken


def max_disjoint_by_start(iv):
    """The tempting rule that is wrong: keep the earliest-STARTING compatible one."""
    taken, last_end = 0, float("-inf")
    for s, e in sorted(iv):
        if s > last_end:
            taken += 1
            last_end = e
    return taken


def brute(iv):
    for k in range(len(iv), 0, -1):
        for combo in combinations(sorted(iv), k):
            if all(combo[i][1] < combo[i + 1][0] for i in range(k - 1)):
                return k
    return 0


bad = [[1, 100], [2, 3], [4, 5], [6, 7]]
print("intervals      ", bad)
print("by end (right) ", max_disjoint_by_end(bad), " optimum:", brute(bad))
print("by start (wrong)", max_disjoint_by_start(bad), " <- one greedy meeting ate the day")
assert max_disjoint_by_end(bad) == 3 and max_disjoint_by_start(bad) == 1

rng = random.Random(9)
for _ in range(300):
    iv = [[s, s + rng.randint(0, 4)]
          for s in (rng.randint(0, 12) for _ in range(rng.randint(0, 7)))]
    assert max_disjoint_by_end(iv) == brute(iv), iv
print("300 random instances: sorting by end is optimal, checked against every subset")
print("minimum removals for", bad, "=", len(bad) - max_disjoint_by_end(bad))
```

Why sorting by end is optimal is a one-paragraph [[greedy-exchange|exchange
argument]]. Let `g₁` have the smallest end, and let `O` be any optimal solution
with `o₁` its earliest-ending member. Then `e(g₁) <= e(o₁)`, so every other
interval of `O` starts after `e(o₁) >= e(g₁)` and does not conflict with `g₁`
either: swapping `o₁` for `g₁` keeps `O` valid and the same size. Recurse on the
intervals starting after `e(g₁)`; after at most `|O|` swaps an optimal solution
has become the greedy's, so the greedy is optimal.

## Recognising it in a statement

Ordered by how much you should trust them.

1. **The input is literally pairs of endpoints.** "`intervals[i] = [start_i,
   end_i]`", "the inclusive start and end times", "`[s, e]` with `s <= e`". Two
   numbers per row and an order on them is the signal; everything else is which
   of the four questions is being asked.
2. **"Overlap", "merge", "conflict", "at the same time", "concurrent",
   "simultaneously".** *Maximum Concurrent Processes*, *Meeting Concurrency
   Intervals*, *Detect a Server RAM Capacity Breach* — all peak-counting.
3. **"Minimum number of X to handle all Y"** — room, core, chair, classroom,
   worker. *Get Minimum Cores*, *Minimum Classrooms for Courses*: the answer is
   the maximum overlap, by the second proof. The highest-frequency shape here.
4. **"Non-overlapping", "the fewest to remove", "the most you can attend".**
   Subset selection, sort by end.
5. **A range of something that is not time.** Card numbers in *Card Range
   Obfuscation Part1*, addresses in *Memory Allocator*, character spans in
   *Highlight Matching Phrases*, the stretch a lamp illuminates in *Lamps
   Illumination*. The word "interval" never appears; the structure is identical.
6. **Constraint shapes.** `n <= 10⁵` with coordinates up to `10⁹` says sort and
   sweep; coordinates up to `10⁵`, or a fixed day of 1440 minutes, says a
   difference array will do and you can skip the sort.

The anti-signals:

- **Pairs that are not ranges.** `(u, v)` as a relation is [[graphs]] or
  [[union-find]]. Ask whether `s <= e` is even meaningful.
- **"Subarray" or "substring".** A contiguous window is [[sliding-window]]
  territory even though a window is an interval: there the windows are not given
  to you, you are choosing them.
- **Weights on the intervals.** Once the objective is a sum of values rather than
  a count, the earliest-end greedy is unsound and you are in DP.
- **Rooms that are not interchangeable.** *Minimum Meeting Rooms with
  Assignments* looks exactly like *Meeting Rooms II* and is not, because the
  achievability half of the proof no longer holds.

## Traps

**Overwriting the block end instead of maximising it.** Symptom: nested
intervals vanish, coverage comes out too small, and the output can even contain
overlapping blocks — which is a property you can assert against.

**Aliasing the caller's rows.** `out.append(interval)` puts the caller's own list
in your result, and the next `out[-1][1] = …` mutates their input. Symptom: right
the first time, different the second time on the same data. Append `[s, e]`.

**Getting the convention wrong at touching endpoints.** `[1,2]` and `[2,3]`: one
merged block or two, one room or two? Closed intervals merge on `s <= ce` and
need 2 rooms, since both meetings own the instant 2; half-open uses `s < ce` and
needs 1. Both are right, only one matches the statement. Symptom: off by exactly
one, only on inputs with a shared endpoint.

**Inclusive length.** *Process Execution Time* says "1 to 5 contributes 5", i.e.
`e - s + 1`, because the units are discrete; a meeting from 1 to 5 o'clock lasts
`e - s = 4` hours, because time is continuous. Decide which world you are in
before writing the sum.

**Event ties in the sweep.** With continuous coordinates, processing the `+1`
before the `-1` at the same `t` reports one room too many. Sort `(t, delta)`
tuples, or work in the `e + 1` half-open form.

**Sorting by end and then merging.** The flush step in the proof needs starts
sorted. Symptom: passes the samples, which tend to arrive sorted by start
already, and fails on shuffled input.

**Forgetting the empty input.** `merge([])` must be `[]`, and the final flush
must not run.

```python run
def merge_right(iv):
    out = []
    for s, e in sorted(iv):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def merge_no_max(iv):                      # bug 1: assigns instead of maximising
    out = []
    for s, e in sorted(iv):
        if out and s <= out[-1][1]:
            out[-1][1] = e
        else:
            out.append([s, e])
    return out


def merge_aliasing(iv):                    # bug 2: stores the caller's own row
    out = []
    for row in sorted(iv):
        if out and row[0] <= out[-1][1]:
            out[-1][1] = max(out[-1][1], row[1])
        else:
            out.append(row)
    return out


nested = [[1, 10], [2, 3], [5, 12]]
print("right  ", merge_right(nested), "covers 1..12, 12 units")
print("no max ", merge_no_max(nested), "<- the block shrank to 3, so 4 fell into a gap")
assert merge_right(nested) == [[1, 12]]
assert merge_no_max(nested) == [[1, 3], [5, 12]]

caller = [[1, 2], [2, 5]]
merge_aliasing(caller)
print("after merge_aliasing, the caller's input is", caller, "<- it was [[1, 2], [2, 5]]")
assert caller == [[1, 5], [2, 5]]

# the same two meetings, the two conventions, two different answers
def rooms(iv, closed):
    ev = []
    for s, e in iv:
        ev.append((s, 1))
        ev.append((e + 1 if closed else e, -1))
    ev.sort()
    cur = best = 0
    for _, d in ev:
        cur += d
        best = max(best, cur)
    return best


touch = [[0, 30], [30, 60]]
print("rooms for", touch, "-> closed (30 is occupied):", rooms(touch, True),
      " half-open (30 is free):", rooms(touch, False))
assert rooms(touch, True) == 2 and rooms(touch, False) == 1
```

The last three lines are the topic's whole bug budget in one print. Neither
answer is a mistake; choosing without noticing there was a choice is.

## What to memorise

Two templates, one sentence, one habit.

**The merge**, which should come out of your fingers:

```python
out = []
for s, e in sorted(intervals):          # by START
    if out and s <= out[-1][1]:         # '<' for half-open intervals
        out[-1][1] = max(out[-1][1], e) # the max is not optional
    else:
        out.append([s, e])              # a copy, not the caller's row
```

**The sweep**, for anything about "how many at once":

```python
ev = [(s, 1) for s, _ in iv] + [(e + 1, -1) for _, e in iv]   # e+1: closed
ev.sort()
cur = best = 0
for _, d in ev:
    cur += d
    best = max(best, cur)
```

**The sentence** that picks the sort: *sort by start to describe the union, sort
by end to choose a subset, and drop the intervals entirely — keeping only tagged
endpoints — to count what is simultaneous.*

**The habit**: before writing anything, write the convention as a comment —
`# closed [s, e], integer minutes` — and normalise to half-open at the door by
replacing `e` with `e + 1`. You will still have to think once; you will not have
to think again in four different places.

Numbers worth carrying: merging `n` intervals yields 1 to `n` blocks and costs
`Θ(n log n)`, optimal in the comparison model; the minimum number of
interchangeable resources equals the maximum overlap; the intersection of
`[a1,a2]` and `[b1,b2]` is `[max(a1,b1), min(a2,b2)]`, non-empty exactly when
`max(a1,b1) <= min(a2,b2)`.

## Check yourself

:::check
The merge scan sorts by start only. Why is it safe to emit a finished block
without ever looking at the intervals that come after the one that closed it?
--
Because the sort gives a one-sided guarantee that is exactly strong enough. When
`[s, e]` has `s > ce` and we flush `[cs, ce]`, every unexamined `[s', e']` has
`s' >= s > ce`, so it lies entirely right of `ce` and cannot touch the block.
That is Case B of the proof.

Note what is *not* guaranteed: nothing about the ends. This is why the same sort
justifies the flush and yet the block end still needs `max(ce, e)`.
:::

:::check
A candidate says: "To pick the largest set of non-overlapping intervals, sort by
start and take each one that does not clash with the last one taken. It is the
same greedy, just a different key." Where are they wrong?
--
The rule is genuinely different and genuinely wrong. On
`[[1,100], [2,3], [4,5], [6,7]]` it takes `[1,100]` first and everything else
clashes, giving 1; sorting by end gives 3. The runnable block above checks the
end rule against every subset on 300 random instances.

The reason is what each rule optimises locally. Taking the earliest end leaves
the resource free as soon as possible, and the exchange argument shows that is
never worse. A small start says nothing about when the resource is released, so
it buys no exchange. Two sorts, two purposes: *starts* describe the union, *ends*
choose a subset.
:::

:::check
*Minimum Meeting Rooms with Assignments* restricts each meeting to a subset of
the rooms. Which half of the "rooms = maximum overlap" proof survives, and what
does that tell you about the answer?
--
The lower bound survives untouched: `M` meetings covering one instant still
pairwise conflict, so you still need at least `M` rooms. The upper bound does
not, because its induction placed each meeting in *any* free room, and with
restrictions the free room may be one this meeting is not allowed to use.

So the sweep gives a valid lower bound and no longer a valid answer — the problem
has become a matching between meetings and permitted rooms, not a counting
problem. Recognising that one sentence of the proof has failed is the whole
difference between this and *Meeting Rooms II*.
:::

:::check
*Process Execution Time* says a process running from 1 to 5 contributes
`5 - 1 + 1 = 5` units. Someone reuses their *Meeting Rooms II* code, which treats
`[s, e]` as half-open, and gets a slightly small answer. Explain the two edits
that fix it, and why there are two.
--
Edit one: the merge test. Half-open code merges only when `s < ce`, so `[1,5]`
and `[5,9]` stay separate, while inclusive units want them merged.

Edit two: the length formula, `e - s + 1` instead of `e - s`.

There are two because the convention leaks into two independent decisions — what
counts as touching, and what a block measures. Converting once at the door
(`e ← e + 1`, then everything is half-open, merge with `s < ce`, length `e - s`)
collapses them into one decision, which is the reason to prefer that style.
:::

:::check
*Insert Interval* hands you an already-sorted, already-disjoint list and one new
interval. Why can it not be solved in `O(log n)`, given that binary search finds
the affected region in `O(log n)`?
--
Because the answer has to be produced. Binary search does locate the affected
region in `O(log n)`, and merging it is `O(k)` in the number of blocks swallowed.
But the specification asks for the full list, and copying the `n - k` untouched
blocks into a new list is `Θ(n)`.

The distinction changes with the interface. If the calendar is a mutable
balanced structure updated in place — the *My Calendar I* setting — then
`O(log n + k)` per insertion is achievable, and over `m` insertions the swallowed
blocks sum to at most `m`, so the amortised cost really is logarithmic. Same
algorithm, different cost, purely because nothing has to be copied.
:::
