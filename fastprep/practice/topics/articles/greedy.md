# Greedy Algorithms

> A greedy algorithm is not "grab the biggest thing". It is a claim — that one
> particular choice can never be the reason you lose — and the algorithm is only
> as good as the proof of that claim.

## When you reach for it

Seven hundred and forty-three problems in this bank are solved greedily, which
makes it the sixth most common topic of a hundred and fifty. Read that number
not as "greedy is a technique" but as: *most optimisation problems that fit in an
interview have a cheap optimal strategy, and the work is finding which one.*

The shape that makes greedy right has three parts, and all three have to hold.

1. **You are asked for an optimum.** A minimum number of operations, a maximum
   number of items, the smallest cost. The bank's titles say it out loud:
   *Minimum Removals for Non-Overlapping Intervals*, *Connect N Ropes With
   Minimum Cost*, *Optimizing Box Weights*.
2. **The decisions can be put in an order, and after you commit to one the rest
   of the problem has the same shape.** Keep an interval, and what remains is
   "schedule the intervals that start after this one ends" — the same problem on
   a smaller input. This is *optimal substructure*.
3. **At the front of that order there is a choice that is never wrong.** Not
   "usually good", not "good on the samples": never wrong, in the sense that some
   optimal solution makes it. This is the *greedy choice property*, and it is the
   one you have to prove.

Part 3 is where greedy problems are won and lost. Writing the code takes four
lines. Knowing whether those four lines are correct takes an argument, and the
argument almost always has the same form: take any optimal solution, find the
first place it disagrees with you, and show you can bend it to agree without
making it worse.

The trigger to look for in a statement is therefore an **asymmetry between
candidates that survives into the future**. Among intervals, the one that ends
earliest leaves strictly the most room for everything after it; there is no way
that being early can hurt you later. Among ropes, the two shortest are the pair
you will pay for the most times, so you want them merged while they are cheap.
When you can name that asymmetry in one sentence, you have a greedy. When you
cannot, you probably have a [[dynamic-programming|DP]].

The anti-trigger is just as concrete: **greedy dies when a choice can be paid
back later, and it dies when there are two resources to trade off against each
other**. A knapsack has a weight budget *and* a value to maximise; the item with
the best value-per-kilo is not always in the optimal set, because taking it can
strand capacity ([[knapsack]]). *Calculate Change* makes change from a fixed list
of bills and coins, and take-the-largest is correct there — but only because that
denomination system is built so that it is. On coins `[1, 3, 4]` the same code is
wrong for the amount 6, and we will watch it be wrong later.

One more limit. A greedy proves the *value* of the optimum, not the identity of
it. If the question is "the lexicographically smallest optimal set", you need a
tie-break rule too, and that rule needs its own argument.

## The idea

Here is the whole subject in one picture. Line up your greedy solution and some
optimal solution side by side, in the order the decisions were made. Walk right
until they first disagree. **Reach into the optimal solution and replace its
choice with yours.** If you can always do that without breaking feasibility and
without making the solution worse, then you can repeat it until the optimal
solution *is* your solution — so yours was optimal all along.

<svg viewBox="0 0 660 210" role="img" aria-label="two rows of choices, optimal and greedy, agreeing on a prefix and swapped at the first disagreement">
  <g>
    <text x="10" y="32">OPT</text>
    <rect class="fill" x="70" y="14" width="60" height="30" rx="4"/>
    <rect class="fill" x="140" y="14" width="60" height="30" rx="4"/>
    <rect x="210" y="14" width="60" height="30" rx="4"/>
    <rect x="280" y="14" width="60" height="30" rx="4"/>
    <rect x="350" y="14" width="60" height="30" rx="4"/>
    <text x="90" y="35">a</text>
    <text x="160" y="35">b</text>
    <text x="232" y="35">o</text>
    <text x="300" y="35">x</text>
    <text x="370" y="35">y</text>
    <text x="10" y="92">GREEDY</text>
    <rect class="fill" x="70" y="74" width="60" height="30" rx="4"/>
    <rect class="fill" x="140" y="74" width="60" height="30" rx="4"/>
    <rect class="fill" x="210" y="74" width="60" height="30" rx="4"/>
    <text x="90" y="95">a</text>
    <text x="160" y="95">b</text>
    <text x="232" y="95">g</text>
    <text x="150" y="130">agree here</text>
    <line x1="210" y1="8" x2="210" y2="112"/>
    <text x="285" y="130">first disagreement</text>
    <line x1="240" y1="52" x2="240" y2="68"/>
    <text x="10" y="172">OPT'</text>
    <rect class="fill" x="70" y="154" width="60" height="30" rx="4"/>
    <rect class="fill" x="140" y="154" width="60" height="30" rx="4"/>
    <rect class="fill" x="210" y="154" width="60" height="30" rx="4"/>
    <rect x="280" y="154" width="60" height="30" rx="4"/>
    <rect x="350" y="154" width="60" height="30" rx="4"/>
    <text x="90" y="175">a</text>
    <text x="160" y="175">b</text>
    <text x="232" y="175">g</text>
    <text x="300" y="175">x</text>
    <text x="370" y="175">y</text>
    <text x="430" y="175">same size, still legal</text>
    <text x="430" y="95">swap o for g</text>
  </g>
</svg>

That picture has a name — the **exchange argument** — and it has a twin called
**greedy stays ahead**, which says the same thing by induction on the prefix
instead of by surgery on the suffix: after `j` decisions, the greedy's state is
at least as good as any optimal solution's state after *its* first `j`
decisions, so the greedy can never run out first.

Everything else is bookkeeping: sort the items by the key that makes the
asymmetry visible, sweep once, and keep a single number describing what you have
committed to so far. If that single number is not enough to decide whether the
next item is legal, you do not have a greedy — you have a DP with a state you
have not written down yet.

## Worked by hand

Take *Minimum Removals for Non-Overlapping Intervals* as stated in this bank:
given intervals, remove the fewest so that no two of the survivors overlap, and
note that intervals which merely touch — one ends exactly where the next begins —
are compatible. Removing the fewest is the same as keeping the most, so we are
picking the largest set of pairwise compatible intervals.

The greedy: **sort by right endpoint and keep an interval whenever it starts at
or after the last kept interval's end.** Here are six intervals, already sorted
by end.

| step | interval | `last_end` before | `start >= last_end`? | action | kept |
| --- | --- | --- | --- | --- | --- |
| 1 | (2, 3) | −∞ | yes | keep, `last_end = 3` | 1 |
| 2 | (1, 4) | 3 | 1 < 3, no | drop | 1 |
| 3 | (3, 5) | 3 | 3 >= 3, yes | keep, `last_end = 5` | 2 |
| 4 | (0, 6) | 5 | 0 < 5, no | drop | 2 |
| 5 | (5, 7) | 5 | 5 >= 5, yes | keep, `last_end = 7` | 3 |
| 6 | (4, 8) | 7 | 4 < 7, no | drop | 3 |

Three kept out of six, so the answer to the stated question is three removals.

<svg viewBox="0 0 660 190" role="img" aria-label="six intervals drawn on a timeline, with the three kept by the earliest-end greedy marked">
  <g>
    <line x1="40" y1="165" x2="620" y2="165"/>
    <text x="40" y="185">0</text>
    <text x="330" y="185">4</text>
    <text x="610" y="185">8</text>
    <rect class="fill" x="185" y="14" width="72" height="16" rx="6"/>
    <text x="270" y="27">(2,3) kept</text>
    <rect x="113" y="42" width="217" height="16" rx="6"/>
    <text x="345" y="55">(1,4) overlaps</text>
    <rect class="fill" x="257" y="70" width="145" height="16" rx="6"/>
    <text x="415" y="83">(3,5) kept</text>
    <rect x="40" y="98" width="362" height="16" rx="6"/>
    <text x="415" y="111">(0,6) overlaps</text>
    <rect class="fill" x="402" y="126" width="145" height="16" rx="6"/>
    <text x="560" y="139">(5,7) kept</text>
    <line x1="185" y1="8" x2="185" y2="170"/>
    <line x1="402" y1="64" x2="402" y2="170"/>
  </g>
</svg>

Four things in that trace are worth pausing on, and none of them is visible in
the code.

**The state is one number.** `last_end` is the entire memory of the algorithm.
Everything about the first five decisions that could possibly matter to the
sixth is compressed into "the timeline is free from 7 onwards". That compression
is what makes a greedy possible; when a problem needs two numbers to describe
the commitment, you are usually looking at a DP table with two indices.

**Step 3 shows what "best" really means.** At step 3 the candidates still
untouched are (3,5), (0,6), (5,7) and (4,8). The greedy takes (3,5), which is
neither the longest, nor the earliest starting, nor the one with the most slack
before it. It is the one that finishes soonest, because the only currency that
matters is *how much timeline is left afterwards*.

**Step 4 shows the cost of sorting by the wrong key.** (0,6) starts before every
interval we kept except the first. A greedy sorted by start time would have
taken it at step 1 and then been unable to take (2,3) or (3,5) — one interval
instead of three. The key is not a detail of the implementation; the key *is*
the algorithm.

**What is proved is the number, not the set.** In general many optimal sets
exist, and which one comes back is decided by how the sort broke ties. The proof
below shows only that no feasible set is larger than the greedy's. A problem that
asks for a *specific* optimal set — the lexicographically smallest, say — needs a
second argument on top.

## Why it is correct

The temptation is to argue "at each step I make the best move, so the result is
best". That is not an argument, it is a restatement, and it is false in general
— it is exactly what fails on coins `[1, 3, 4]`. Here is the real thing.

:::proof Earliest finishing time is optimal for interval selection
**Setup.** Intervals `I = {(s₁, e₁), …, (sₙ, eₙ)}` with `sᵢ < eᵢ`. Two intervals
are *compatible* if one's start is at least the other's end. A *feasible* set is
one whose members are pairwise compatible; write any feasible set in increasing
order of end time. The greedy scans `I` sorted by end time, keeping an interval
iff its start is at least the end of the last kept one; call its output
`g₁, …, g_k` in the order chosen — which is also increasing in end time.

**Claim (greedy stays ahead).** Let `o₁, …, o_m` be *any* feasible set, written
in increasing order of end time. Then for every `j` with `1 <= j <= m`, the
greedy has selected at least `j` intervals, and `end(g_j) <= end(o_j)`.

**Base case, `j = 1`.** The greedy's first kept interval is the first one it
meets, which is the interval of `I` with the globally smallest end time. Since
`o₁ ∈ I`, `end(g₁) <= end(o₁)`. And `k >= 1` because `I` is non-empty.

**Inductive step.** Assume `k >= j` and `end(g_j) <= end(o_j)`, and assume
`m >= j + 1`, so `o_{j+1}` exists. Since `o_j` and `o_{j+1}` are compatible,
`start(o_{j+1}) >= end(o_j) >= end(g_j)`, and since intervals are non-empty,
`end(o_{j+1}) > start(o_{j+1}) >= end(g_j)`. Two facts follow.

`o_{j+1}` strictly follows `g_j` in end order, so when the greedy commits to
`g_j` the interval `o_{j+1}` is still ahead of the scan; and it is *legal*, since
its start is at or after `last_end = end(g_j)`. Therefore the greedy does not
stop with `j` intervals — at worst it reaches `o_{j+1}` and takes it — so
`k >= j + 1`. And because the greedy keeps the *first* legal interval it meets
while candidates arrive in increasing end order, `end(g_{j+1}) <= end(o_{j+1})`.
The invariant is restored.

**Termination.** The scan visits each of the `n` intervals exactly once and each
visit is a constant amount of work, so the algorithm halts after `n` steps.

**Conclusion.** Suppose some feasible set had `m > k`. Apply the claim with
`j = k`: it says the greedy selected at least `k` intervals and stayed ahead. Now
apply the inductive step once more with `j = k`, which is legal because
`m >= k + 1`: it concludes `k >= k + 1`, a contradiction. So no feasible set is
larger than `k`, and the greedy output is optimal. ∎
:::

:::note The same proof, said as an exchange
If you prefer surgery to induction: let `O` be an optimal set, and let `g₁` be
the interval with the smallest end time. Let `o₁` be the earliest-ending member
of `O`. Then `end(g₁) <= end(o₁)`, so `O' = (O \ {o₁}) ∪ {g₁}` is still feasible —
every other member of `O` starts at or after `end(o₁) >= end(g₁)` — and has the
same size. So *some* optimal solution makes the greedy's first choice. Delete
`g₁` and everything overlapping it, and repeat on the remainder. That is the
[[greedy-exchange|exchange argument]] in its general form, and it is the tool you
reach for when "stays ahead" has no natural quantity to compare.
:::

Now name what the proof leaned on, because that list is where the bugs live.

- **Feasibility depends only on `last_end`.** The step "so `o_{j+1}` is still
  legal for the greedy" used nothing about which intervals the greedy had kept,
  only where it had got to. Add a rule like "at most three intervals per hour"
  and this collapses instantly.
- **Every interval is worth exactly one.** The conclusion compared *sizes*. Give
  intervals values and the argument gives you nothing: swapping `o₁` for `g₁`
  preserves the count but can lower the total value. Weighted interval scheduling
  is a genuine DP, and this is the single most common way a correct greedy becomes
  a wrong one.
- **Sorting by end time is a total order on the candidates.** Ties can be broken
  any way at all — the proof only ever used `<=` — which is why you do not need a
  tie-break rule here. In other greedies you do, and then the tie-break needs its
  own exchange argument.
- **Nothing is compulsory.** No interval is forced into the answer. A constraint
  like "interval 4 must be kept" breaks the base case, because the greedy's first
  pick may be incompatible with it.
- **The comparison is `>=`, matching "touching is compatible".** If the problem
  said touching intervals conflict, every `>=` becomes `>` and the proof goes
  through unchanged with the modified definition — but the *answers* change.

## What it costs

Derive it rather than quoting it. The algorithm is a sort followed by a single
pass, and the pass does a constant amount of work per item:

    T(n) = sort(n) + n · O(1) = Θ(n log n) + Θ(n) = Θ(n log n)

so the sort dominates, and it dominates by a full logarithmic factor. Two
immediate consequences. If the input arrives already sorted — by deadline, by
arrival time, by index — the greedy is **Θ(n)**, and you should say so rather
than reflexively claiming `n log n`. And if you are tempted to replace the sort
with something cleverer, do not bother unless you can also remove it: an `O(n)`
counting sort over small integer keys ([[counting-sort]]) is the only thing that
actually changes the exponent here, and it needs a bounded key range.

Space is `O(1)` beyond the sort if you are allowed to sort in place and only
need the count, or `O(k)` if you must return the kept items.

**A heap greedy costs differently, and the derivation is worth doing.** In
*Connect N Ropes With Minimum Cost* you repeatedly merge the two shortest ropes
and pay their sum. Each merge pops two and pushes one, so the heap shrinks by one
per merge and there are exactly `n − 1` merges. Merge number `i` operates on a
heap of size at most `n`, so it costs `3 log n` comparisons at worst:

    T(n) = Σ_{i=1}^{n-1} O(log n) = Θ(n log n)

with `Θ(n)` space for the heap.

**A scan greedy can have no sort at all.** *Jump Game II* asks for the fewest
jumps to the end of an array where `nums[i]` is how far you may move from `i`.
The greedy keeps two numbers: the end of the range reachable with the current
number of jumps, and the farthest index reachable with one more. Each index is
touched exactly once and updates both numbers in `O(1)`, so by a counting
argument the total is **Θ(n)** with `O(1)` space. The order is given by the
problem, so there is nothing to sort — a useful reminder that "greedy" and
"sorting" are correlated, not synonymous.

**The cost people forget** is the key, not the loop. Three versions of it:

- *Comparator cost.* Sorting by a key you compute inside the comparator computes
  it `O(n log n)` times. Compute it once into a tuple. See
  [[custom-comparators]].
- *The feasibility check.* When the greedy is used as the inner check of a
  [[binary-search-on-answer]] — *Aggressive Cows* is the standard example: binary
  search the minimum spacing, and greedily place each cow at the first stall far
  enough along — the total is `O(n log(range))` because the `O(n)` greedy runs
  once per candidate answer. People quote the greedy's cost and forget the outer
  loop multiplies it.
- *Verification.* Not runtime, but the cost you should pay anyway: a brute-force
  cross-check on tiny inputs, fifteen lines, and the only thing standing between
  a plausible greedy and a wrong submission.

## The implementation

```python run
from itertools import combinations
import random


def keep_max_compatible(intervals):
    """Largest set of pairwise non-overlapping intervals; touching is allowed."""
    kept, last_end = [], None
    for s, e in sorted(intervals, key=lambda iv: iv[1]):     # the key IS the algorithm
        if last_end is None or s >= last_end:                # legal given one number
            kept.append((s, e))
            last_end = e                                     # the whole state update
    return kept


def min_removals(intervals):
    return len(intervals) - len(keep_max_compatible(intervals))


def brute_force_best(intervals):
    """Exponential ground truth: the largest feasible subset, by inspection."""
    for k in range(len(intervals), -1, -1):
        for combo in combinations(intervals, k):
            ordered = sorted(combo, key=lambda iv: iv[0])
            if all(b[0] >= a[1] for a, b in zip(ordered, ordered[1:])):
                return k
    return 0


demo = [(1, 4), (2, 3), (3, 5), (0, 6), (5, 7), (4, 8)]
kept = keep_max_compatible(demo)
print("intervals :", demo)
print("kept      :", kept)
print("removals  :", min_removals(demo))
assert kept == [(2, 3), (3, 5), (5, 7)]
assert min_removals(demo) == 3

rng = random.Random(4)
for _ in range(400):                       # the habit: prove it against brute force
    n = rng.randint(0, 8)
    ivs = []
    for _ in range(n):
        s = rng.randrange(0, 12)
        ivs.append((s, s + rng.randint(1, 5)))
    assert len(keep_max_compatible(ivs)) == brute_force_best(ivs), ivs
print("400 random instances (n <= 8) match the exhaustive optimum")
```

Three lines carry the chapter.

`sorted(intervals, key=lambda iv: iv[1])` is the entire design decision. Change
`iv[1]` to `iv[0]` and the code still runs, still terminates, still returns a
feasible set, and is wrong. There is no assertion you can add inside the loop
that will catch it; the only defence is the proof or the brute-force check.

`if last_end is None or s >= last_end` is the feasibility test, and it is a test
against **one number**. When you are deciding whether a problem is greedy, try
writing this line first. If you cannot write it without referring to more of the
history, stop and reach for [[dynamic-programming]].

The `assert ... == brute_force_best(ivs)` loop is not about intervals at all.
Four hundred random instances of size at most eight refute essentially every
wrong greedy you can invent, in under a second. It is the difference between "I
think this is greedy" and "this is greedy".

## Variants you will meet

**Sort, then sweep with one state variable.** The form above. The family is
enormous; what changes is the sort key. By end time for interval selection
([[intervals]]); by deadline for scheduling ([[scheduling]]); by size for
*Optimizing Box Weights*, where you sort descending and take items until your
subset outweighs the rest — correct because the `k` heaviest items maximise the
sum of any `k`-subset, so if any subset of size `k` can win, that one does.

**Longest run after sorting.** *An Evening of Movies* wants the longest sequence
of distinct movies where each runtime equals the previous or is exactly one
minute longer. Sort the runtimes and take the longest block whose consecutive
differences are all 0 or 1: the sort plus a linear sweep.

**Heap greedy — repeatedly take the two extremes.** *Connect N Ropes With
Minimum Cost*. The exchange argument here is about depth: a rope's length is paid
once per merge it participates in, so the longest ropes must sit at the shallowest
depth, which is exactly what merging the two smallest first achieves. This is
[[huffman]] coding wearing work clothes, and it needs a [[heap]].

**Stay-ahead greedy on a given order.** *Jump Game II*; also the classic
"gas station" shape. Nothing is sorted; the invariant is "after `j` jumps I can
reach at least as far as any other strategy can after `j` jumps", proved by
induction on `j`.

**Two-pointer greedy.** *Container With Most Water*: move the pointer at the
shorter wall, because that wall caps every pair it belongs to, so discarding it
cannot discard the optimum. Same exchange argument, different clothes —
[[two-pointers]].

**Counting greedy with a closed form.** *Task Scheduler* — schedule tasks with a
cooldown of `n` between equal labels. Lay out the most frequent task first,
`maxFreq − 1` blocks of width `n + 1`, then fit everything else into the gaps.
The answer is `max(total_tasks, (maxFreq − 1) · (n + 1) + how_many_tasks_hit_maxFreq)`:
the first term because you can never take fewer intervals than you have tasks,
the second because the skeleton of the most frequent task is forced.

**Sweep-line greedy.** *Minimum Number of Chairs* wants the peak number of guests
present at once: turn each guest into `+1` at arrival and `−1` at departure, sort
the events, take the running maximum. See [[sweep-line]].

**Greedy as the predicate of a binary search.** *Aggressive Cows*, and every
"minimise the maximum" statement. The greedy answers *is this candidate
feasible?*, the binary search finds the boundary: [[binary-search-on-answer]].

**Lexicographic greedy.** *Biggest Number From Digits*, *Get Alphabetically
Smallest String*: fix the leftmost position first, because any improvement at an
earlier position outweighs everything after it. These frequently need a
[[monotonic-stack]] to make "the best feasible character here" cheap.

```python run
import heapq
from functools import lru_cache
import random


def connect_cost(ropes):
    """Merge the two shortest ropes repeatedly; pay the sum each time."""
    heap = list(ropes)
    heapq.heapify(heap)
    total = 0
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        total += a + b
        heapq.heappush(heap, a + b)
    return total


@lru_cache(maxsize=None)
def best_cost(state):
    """Ground truth: try every possible pair to merge, at every stage."""
    if len(state) <= 1:
        return 0
    best = None
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            rest = list(state[:i]) + list(state[i + 1:j]) + list(state[j + 1:])
            merged = state[i] + state[j]
            cost = merged + best_cost(tuple(sorted(rest + [merged])))
            best = cost if best is None else min(best, cost)
    return best


demo = (1, 2, 5, 10, 35, 89)
print("ropes            :", demo)
print("greedy total cost:", connect_cost(demo))
print("exhaustive best  :", best_cost(tuple(sorted(demo))))
assert connect_cost(demo) == best_cost(tuple(sorted(demo)))

# the cost is sum(length * number of merges it survives), which is why the
# shortest ropes must be merged first: they are the ones paid for most often
rng = random.Random(9)
for _ in range(60):
    n = rng.randint(1, 6)
    ropes = tuple(rng.randint(1, 30) for _ in range(n))
    assert connect_cost(ropes) == best_cost(tuple(sorted(ropes))), ropes
print("60 random rope sets: always-merge-the-two-smallest is exactly optimal")
```

## Recognising it in a statement

Ordered by how much you should trust them.

1. **"Minimum number of operations / moves / removals / swaps" with independent
   operations.** More than a hundred titles in this bank start with *Minimum* or
   *Maximize*. When each operation's effect does not depend on which other
   operations you chose, there is almost certainly a local rule.
2. **The statement hands you a natural order and a single running quantity.**
   Times, deadlines, positions along a line, sorted weights — plus one thing you
   are tracking (the last end, the current reach, the remaining budget).
3. **"The tasks may be done in any order."** An explicit licence to sort. Without
   it, check whether the order is part of the problem.
4. **Divisible or interchangeable items.** Fractions make greedy work where
   integrality breaks it; this is the whole difference between fractional and
   0/1 knapsack.
5. **`n` up to 10⁵ or 2·10⁵ with an optimisation objective.** Exponential search
   and an `O(n²)` DP are both out, so the intended solution is `O(n log n)` — the
   shape of sort-then-sweep. Weak on its own, since [[binary-search-on-answer]]
   has the same shape, but it narrows the field fast.

The anti-signals, which are more valuable than the signals:

- **A second budget.** "At most `k` removals", "within capacity `W`", "using at
  most `m` machines" alongside a value to optimise. Two dimensions is the
  signature of a DP table.
- **Items carry weights or values.** Interval selection is greedy; interval
  selection with profits is DP. The moment the objective stops being "how many",
  re-derive from scratch.
- **"Count the number of ways."** Greedy answers "what is the best"; counting is
  [[counting-dp]] or [[combinatorics]].
- **Decisions that can be revisited.** If the statement lets you undo, or if the
  effect of a choice depends on a later choice, the exchange argument has nothing
  to exchange.
- **Custom, arbitrary denominations or costs.** *Calculate Change* is greedy
  because real currency is designed to be; a made-up coin system is a DP.

## Traps

**Sorting by the intuitive key instead of the provable one.** Shortest-first and
earliest-start-first both feel reasonable for interval selection and both are
wrong. Symptom: correct on the samples, wrong when one long interval swallows
several short ones.

**Trusting the samples.** Three examples are three points of an infinite space,
and greedy failures are usually rare rather than obvious. Symptom: a confident
submission, a wrong answer on test 47. Cure: the brute-force loop above.

**Applying a greedy that is only correct for a special input class.** Largest
coin first is optimal for *canonical* coin systems and nothing else. Symptom: the
answer is off by one coin on a handful of amounts.

**Tie-breaks that change the answer.** If two orderings of equal-key items give
different results, your proof has a hole: a correct greedy either ignores ties or
has an argument for the rule it uses.

**Half-open versus closed comparisons.** `s >= last_end` and `s > last_end` are
different algorithms. *Minimum Removals for Non-Overlapping Intervals* says
touching intervals are compatible, and *Minimum Number of Chairs* says a guest
leaving at `t` frees a chair for one arriving at `t` — the same convention in
sweep-line form. Read the sentence; do not guess.

**Floating point in a greedy over money.** *Calculate Change* deals in values
like `0.05`; comparisons and subtractions in binary floating point will drift.
Work in integer cents. See [[numerical-stability]].

**Committing when you meant to simulate.** A greedy never backtracks. If your
code says "try this, and if it fails go back", it is [[backtracking]] and its
cost is not `O(n log n)`.

```python run
def greedy_intervals(intervals, key):
    kept, last_end = [], None
    for s, e in sorted(intervals, key=key):
        if last_end is None or s >= last_end:
            kept.append((s, e))
            last_end = e
    return kept


by_end = lambda iv: iv[1]
by_start = lambda iv: iv[0]
by_length = lambda iv: iv[1] - iv[0]

trap_a = [(0, 10), (1, 2), (3, 4), (5, 6)]
print("intervals       :", trap_a)
print("by end (correct):", greedy_intervals(trap_a, by_end))
print("by start (wrong):", greedy_intervals(trap_a, by_start), "one greedy interval eats three")
assert len(greedy_intervals(trap_a, by_end)) == 3
assert len(greedy_intervals(trap_a, by_start)) == 1

trap_b = [(0, 5), (4, 6), (5, 10)]
print()
print("intervals        :", trap_b)
print("by end (correct) :", greedy_intervals(trap_b, by_end))
print("by length (wrong):", greedy_intervals(trap_b, by_length), "the short one blocks both others")
assert len(greedy_intervals(trap_b, by_end)) == 2
assert len(greedy_intervals(trap_b, by_length)) == 1


def coins_greedy(coins, amount):
    n = 0
    for c in sorted(coins, reverse=True):
        take = amount // c
        n += take
        amount -= take * c
    return n if amount == 0 else None


def coins_dp(coins, amount):
    INF = float("inf")
    best = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1
    return None if best[amount] == INF else best[amount]


print()
print("coins [1,3,4], amount 6 -> greedy:", coins_greedy([1, 3, 4], 6),
      "coins, optimal:", coins_dp([1, 3, 4], 6), "coins (3+3)")
print("coins [1,5,10,25], amount 30 -> greedy:", coins_greedy([1, 5, 10, 25], 30),
      "coins, optimal:", coins_dp([1, 5, 10, 25], 30), "coins (25+5)")
assert coins_greedy([1, 3, 4], 6) == 3 and coins_dp([1, 3, 4], 6) == 2
assert coins_greedy([1, 5, 10, 25], 30) == coins_dp([1, 5, 10, 25], 30) == 2
for amount in range(0, 200):          # canonical system: greedy is optimal everywhere
    assert coins_greedy([1, 5, 10, 25], amount) == coins_dp([1, 5, 10, 25], amount)
print("same code, same shape: correct on one coin system, wrong on the other")
```

## What to memorise

Not a solution. A shape, a sentence and a habit.

**The shape**, which should come out of your fingers:

```python
items.sort(key=...)          # the key is the whole design decision
state = initial
result = 0
for it in items:
    if feasible(state, it):  # a test against ONE number, or it is not greedy
        result += 1
        state = update(state, it)
```

**The sentence** that turns a problem into it: *"If I take this item now, can I
bend any optimal solution to agree with me — swap its choice for mine — without
making it worse or illegal?"* If yes, you have a greedy and you have just written
its proof. If you cannot say it, you do not have one yet.

**The habit**: write the brute force first, on inputs of size eight, and run a
few hundred random cases against your greedy before you trust it. This is the one
family where a plausible wrong answer is the default outcome.

Three things worth carrying. Sort-then-sweep is `Θ(n log n)` and the sort is the
whole cost, so an already-ordered input makes it linear. A second budget in the
statement — a capacity, a count limit, a value alongside a count — means DP until
proven otherwise. And the two proof templates, *stays ahead* and *exchange*, are
interchangeable: if one refuses to go through, try the other before concluding
the greedy is wrong.

## Check yourself

:::check
For interval selection, why does sorting by *earliest end* work when sorting by
*shortest length* does not? Answer in terms of the invariant, not in terms of
examples.
--
Because the state of the algorithm is a single number, `last_end`, and the only
thing a choice does to the future is push that number forward. Among all legal
candidates at a given moment, the one with the smallest end pushes `last_end` the
least, so the set of intervals legal afterwards is a superset of what any other
choice leaves. That is exactly the inductive step of the proof: `end(g_j)` stays
at or below `end(o_j)` for every `j`.

Shortest length optimises a quantity that never appears in the state. A short
interval that starts late — `(9, 10)` when the alternative is `(0, 3)` — pushes
`last_end` to 10 and destroys more of the future than a longer, earlier one. The
rule for choosing a greedy key: it must be the quantity the *state* is made of,
not the quantity the items are made of.
:::

:::check
Someone says: "My greedy is right — it passes every sample, it is `O(n log n)`
which matches the constraint `n <= 2·10^5`, and the problem is clearly a greedy
problem." Where are they wrong?
--
In three places, and the third is the interesting one.

Passing the samples is evidence about three inputs. Greedy failures are usually
not adversarial but merely uncommon; the coin block above shows that `[1,5,10,25]`
agrees with the optimum on every amount while `[1,3,4]` disagrees at 6. You
cannot sample your way to a proof.

Matching the complexity bound is a signal about the *intended* solution's shape,
not about this code's correctness: a sort plus a [[two-pointers]] sweep, a
[[binary-search-on-answer]] and a heap sweep all cost `O(n log n)` too.

And "clearly a greedy problem" is the real error: greedy is not a property of a
problem, it is a property of a *problem together with a specific rule*. Interval
selection is greedy by earliest end and not greedy by earliest start. The claim
that needs support is never "this is greedy" but "*this rule* is optimal", which
is one exchange argument.
:::

:::check
Attach a profit to each interval and ask for the maximum total profit from a
compatible set. Point at the exact line of the proof that fails, and say what
replaces the algorithm.
--
The conclusion. Everything up to and including "greedy stays ahead" survives:
`end(g_j) <= end(o_j)` is still true, because it is a statement about end times
and the greedy still picks the earliest-ending legal interval. What breaks is the
final step, which converted "the greedy selected at least as many intervals" into
"the greedy is optimal". With profits, `k >= m` says nothing — three intervals
worth 1 each lose to one interval worth 100.

The exchange phrasing fails at the same point: swapping `o₁` for `g₁` keeps the
set feasible and keeps its *size*, but can lower its *value*.

What replaces it is weighted interval scheduling: sort by end, and for each
interval `i` let `p(i)` be the last interval that ends at or before `i` starts
(found by [[binary-search|binary search]]). Then
`best[i] = max(best[i-1], profit[i] + best[p(i)])` — every optimal solution either
uses interval `i` or does not, and both branches are covered. `O(n log n)`, and it
is [[dp-1d]], not greedy.
:::

:::check
*Aggressive Cows* is solved by a binary search whose feasibility check is itself
a greedy. Is that circular — using an unproven greedy inside a search? Explain
why the two arguments are independent, and give the complexity.
--
It is not circular, because the greedy inside proves a *different* statement from
the one the search needs.

The inner greedy answers: given a required minimum spacing `d`, can all the cows
be placed? Walk the stalls in sorted order and place a cow at the first stall at
least `d` beyond the last placed cow. The exchange argument is local: if some
feasible placement puts its `i`-th cow further right than the greedy does, sliding
that cow left to the greedy's stall keeps every later gap at least as large, so
feasibility is preserved. Hence the greedy places the maximum possible number of
cows for that `d`, and "greedy places them all" is equivalent to "a placement
exists".

The outer binary search needs only that feasibility is *monotone* in `d`: if
spacing `d` is achievable then so is any smaller spacing, since the same placement
works. That is an argument about the problem, not about the greedy.

Cost: the check is `O(n)` after one `O(n log n)` sort, and it runs `O(log R)`
times for a position range `R`, giving `O(n log n + n log R)`.
:::

:::check
You have written a greedy and a brute force, and on one random input of size six
they disagree. Before you change the greedy, what are the two other things that
could be wrong, and how do you tell them apart?
--
First, the brute force. It is the thing you are treating as ground truth, so a
bug in it is a bug in your definition of the answer — and brute forces get
feasibility checks wrong all the time (the `>=` versus `>` question is the usual
culprit, and it bites both programs in different places). Check it by hand on the
failing input: six items is small enough to enumerate on paper.

Second, the problem statement. If the greedy and the brute force encode different
readings of the rules — one treating touching intervals as compatible and the
other not, or one allowing an item to be reused — they will disagree on exactly
the inputs that distinguish the readings. The signature is that the failing input
is *minimal and structured* (it contains a tie, a touch, a zero, an empty set)
rather than random-looking.

Only when both survive is the greedy itself wrong, and then the failing input is
a gift: it is a counterexample to the exchange argument you thought you had, and
looking at where the two solutions first diverge tells you which choice was not
safe.
:::
