# Proving Greedy: Exchange Arguments

> An exchange argument never claims the greedy choice is the best one. It shows
> that any optimal solution can be bent, one decision at a time, into the greedy
> one without ever breaking or getting worse — which is a far easier thing to
> prove.

## When you reach for it

You reach for this the moment you have a greedy rule and a doubt. Not before:
inventing the rule is [[greedy]]'s job. This chapter is about what decides
whether that rule is a solution or a plausible-looking wrong answer.

Five hundred and eighty-six problems in this bank are greedy, the seventh most
common topic of a hundred and fifty. That number is a warning as much as an
invitation: greedy code is short, so it gets written fast, and a wrong greedy
passes the two sample cases roughly as often as a right one. The only thing
separating them is an argument.

The method applies when you can describe your algorithm as a **sequence of
decisions** — take this interval, merge these two ropes, jump to this index — and
can say what it would mean for some other solution to make the *same* decision.
That is all it needs; it does not care whether the decisions come from a sort, a
heap or a scan.

It is the wrong tool in two situations. The first is when a decision's
consequences cannot be summarised by anything small: 0/1 [[knapsack]] makes you
carry a whole remaining-capacity dimension, and no single swap repairs a solution
that disagrees with you. The second, more insidious, is when items carry
**weights** unrelated to the resource they consume. *Meeting Room* is exactly the
interval problem this chapter proves, except that each group brings `people[i]`
along and you must minimise the people left out. Every step of the proof below
survives that change except one — the step saying a swap keeps the value the same
— and that single failure is the difference between a four-line greedy and a
dynamic program. When the argument breaks, it usually breaks at a place that
tells you what to write instead.

The problems where it works are everywhere. *Minimum Removals for Non-Overlapping
Intervals* is the textbook case in disguise: "remove the minimum number of
intervals so that every pair of remaining intervals is non-overlapping" is `n`
minus "keep the maximum number of compatible intervals". *Connect N Ropes With
Minimum Cost* and *Array Reduction 1* are one problem told twice — pay the sum of
the two things you merge — and the exchange for both is the one Huffman used.

## The idea

Write your greedy's output as a list of decisions `g1, g2, …, gk`. Take any
optimal solution `S` and write it in the same order. Now walk the two lists in
parallel until they first disagree, at position `j+1`.

**Reach into `S`, pull out its choice at that position, and put greedy's choice
there instead.**

If you can show that the result is still legal and still just as good, you have
manufactured a new optimal solution that agrees with greedy one step further
along. Do it again. And again. The number of leading agreements only goes up, and
it cannot exceed `k`, so after at most `k` repairs the optimal solution *is*
greedy's. Greedy was optimal all along.

<svg viewBox="0 0 640 205" role="img" aria-label="two rows of decisions, an optimal solution above and greedy below, agreeing on a prefix and differing at the next position where a swap is applied">
  <g>
    <text x="155" y="22" text-anchor="middle">they already agree</text>
    <line x1="60" y1="30" x2="250" y2="30"/>
    <text x="30" y="62">S</text>
    <rect x="60" y="40" width="90" height="34" rx="4"/>
    <text x="105" y="63" text-anchor="middle">g1</text>
    <rect x="160" y="40" width="90" height="34" rx="4"/>
    <text x="205" y="63" text-anchor="middle">g2</text>
    <rect x="260" y="40" width="90" height="34" rx="4"/>
    <text x="305" y="63" text-anchor="middle">t</text>
    <rect x="360" y="40" width="90" height="34" rx="4"/>
    <text x="405" y="63" text-anchor="middle">rest of S</text>
    <line x1="305" y1="80" x2="305" y2="124"/>
    <line x1="305" y1="124" x2="298" y2="112"/>
    <line x1="305" y1="124" x2="312" y2="112"/>
    <text x="325" y="106">swap</text>
    <text x="30" y="152">G</text>
    <rect x="60" y="130" width="90" height="34" rx="4"/>
    <text x="105" y="153" text-anchor="middle">g1</text>
    <rect x="160" y="130" width="90" height="34" rx="4"/>
    <text x="205" y="153" text-anchor="middle">g2</text>
    <rect class="fill" x="260" y="130" width="90" height="34" rx="4"/>
    <text x="305" y="153" text-anchor="middle">g3</text>
    <rect x="360" y="130" width="90" height="34" rx="4"/>
    <text x="405" y="153" text-anchor="middle">rest of G</text>
    <text x="20" y="195">each swap buys one more agreement, and agreement is bounded</text>
  </g>
</svg>

Notice the direction. You are not showing greedy can be improved into the
optimum; you are showing the optimum can be *degraded* into greedy without losing
anything. That asymmetry is the whole trick, and it is why the argument is easy:
you get to assume you hold a perfect solution, and need only prove that one small
act of vandalism does not hurt it.

Three obligations come out of that picture, and a complete proof discharges all
three:

1. **Feasibility.** After the swap, the solution is still legal.
2. **No loss.** Its value is no worse (for a minimisation, its cost is no
   higher).
3. **Progress.** It agrees with greedy on strictly more leading decisions.

Most wrong greedy proofs quietly skip obligation 1 or 2; most wrong greedy
*algorithms* are ones where obligation 1 or 2 is actually false. Writing the
proof is how you find out which you have.

## Worked by hand

Seven intervals, from a *Minimum Removals for Non-Overlapping Intervals*-shaped
instance. Touching is allowed — an interval that ends at 4 and one that starts at
4 may both stay, exactly as that statement specifies.

```
(1,4) (2,4) (0,6) (4,7) (5,8) (7,10) (8,11)
```

The greedy rule: sort by **finish** time, scan, and take an interval whenever it
starts at or after the last finish taken.

<svg viewBox="0 0 640 250" role="img" aria-label="seven intervals drawn as horizontal bars on a time axis, with three of them highlighted as greedy's choices">
  <g>
    <rect class="fill" x="85" y="30" width="135" height="14" rx="3"/>
    <text x="228" y="42">(1,4) taken</text>
    <rect x="130" y="56" width="90" height="14" rx="3"/>
    <text x="228" y="68">(2,4) skipped</text>
    <rect x="40" y="82" width="270" height="14" rx="3"/>
    <text x="318" y="94">(0,6) skipped</text>
    <rect class="fill" x="220" y="108" width="135" height="14" rx="3"/>
    <text x="363" y="120">(4,7) taken</text>
    <rect x="265" y="134" width="135" height="14" rx="3"/>
    <text x="408" y="146">(5,8) skipped</text>
    <rect class="fill" x="355" y="160" width="135" height="14" rx="3"/>
    <text x="498" y="172">(7,10) taken</text>
    <rect x="400" y="186" width="135" height="14" rx="3"/>
    <text x="543" y="198">(8,11) skipped</text>
    <line x1="40" y1="215" x2="580" y2="215"/>
    <line x1="40" y1="210" x2="40" y2="220"/>
    <line x1="220" y1="210" x2="220" y2="220"/>
    <line x1="400" y1="210" x2="400" y2="220"/>
    <line x1="580" y1="210" x2="580" y2="220"/>
    <text x="36" y="235">0</text>
    <text x="216" y="235">4</text>
    <text x="396" y="235">8</text>
    <text x="574" y="235">12</text>
  </g>
</svg>

The scan, with `last` the finish time of the most recent interval taken:

| step | interval | `last` before | `start >= last`? | action | kept so far |
| --- | --- | --- | --- | --- | --- |
| 1 | (1,4) | −∞ | yes | take | (1,4) |
| 2 | (2,4) | 4 | 2 < 4, no | skip | (1,4) |
| 3 | (0,6) | 4 | 0 < 4, no | skip | (1,4) |
| 4 | (4,7) | 4 | 4 ≥ 4, yes | take | (1,4) (4,7) |
| 5 | (5,8) | 7 | 5 < 7, no | skip | (1,4) (4,7) |
| 6 | (7,10) | 7 | 7 ≥ 7, yes | take | (1,4) (4,7) (7,10) |
| 7 | (8,11) | 10 | 8 < 10, no | skip | (1,4) (4,7) (7,10) |

Three kept, so four removals.

The trace says three things the code does not.

**Step 4 and step 6 are the whole rule.** Both were accepted on equality:
`4 >= 4`, `7 >= 7`. If the problem had said overlapping endpoints conflict, the
one character `>=` becomes `>` and the answer changes. The statement's sentence
about intervals that touch is not decoration; it is the comparator.

**Step 3 is where greedy proves it is not a heuristic.** Nothing forced us to
reject `(0,6)`; an algorithm scanning by *start* time would have grabbed it first
and finished with only two intervals, `(0,6)` and `(7,10)`. Greedy skipped it
because it finishes late, and finishing late is the only thing that costs
anything. The quantity optimised at each step is not "how many have I taken" but
**how much of the timeline is still free**.

**The state after any prefix is a single number.** After step 4 the algorithm
remembers `last = 7` and nothing else — not which intervals it took, not how many
it skipped. That compression is what makes the exchange work: two solutions that
have consumed the same amount of the resource are interchangeable from here on,
whatever they did earlier. When you meet a greedy candidate and cannot compress
its history into one number (or one small tuple), be suspicious.

## Why it is correct

The proof comes in two halves. The first is the schema, which you reuse for every
greedy you will ever write. The second instantiates it on the intervals above, and
is the part you improvise at the whiteboard.

:::proof Exchange schema, and interval scheduling as an instance
**Part 1 — the schema.**

*Setup.* A greedy algorithm makes decisions `g1, …, gk` in a fixed canonical
order and outputs `G = {g1, …, gk}`. Feasible solutions are written in the same
canonical order. Let `val` be the objective, to be maximised. For a feasible `S`,
define the **agreement** `a(S)` = the largest `j` such that the first `j`
decisions of `S` are exactly `g1, …, gj`.

*The two obligations.* Suppose you can prove, for your problem:

- **(E) Exchange.** If `S` is optimal and `a(S) = j < k`, there is a feasible `S'`
  with `val(S') >= val(S)` and `a(S') >= j + 1`.
- **(C) Closure.** Any feasible `S` with `a(S) = k` satisfies `val(S) <= val(G)`.

*Claim.* Then `G` is optimal.

*Base case.* The set of feasible solutions is finite and non-empty (it contains
`G`), so an optimal `S₀` exists, and `a(S₀) >= 0` trivially.

*Inductive step.* Suppose `Sᵢ` is optimal with `a(Sᵢ) = j < k`. Apply (E) to get a
feasible `Sᵢ₊₁` with `val(Sᵢ₊₁) >= val(Sᵢ) = OPT`. Since `OPT` is the maximum over
feasible solutions, `val(Sᵢ₊₁) = OPT`, so `Sᵢ₊₁` is itself optimal, and
`a(Sᵢ₊₁) >= j + 1`.

*Termination.* `a(S₀) < a(S₁) < a(S₂) < …` is a strictly increasing sequence of
integers bounded above by `k`, so at most `k` steps are possible. The process
stops only when the hypothesis of the step fails, i.e. at some optimal `S*` with
`a(S*) = k`.

*Conclusion.* `S*` is optimal, so `val(S*) = OPT`; and by (C), `val(G) >= val(S*)`.
Since `G` is feasible, `val(G) = OPT`.

**Part 2 — interval scheduling.**

*Setup.* Intervals `[s, f]` with `s < f`. Two are compatible if one's finish is
`<=` the other's start. A solution is a pairwise-compatible set; `val` is its
cardinality. Because members of a compatible set are disjoint and non-empty,
their starts and finishes are in the same strict order, so "canonical order" is
unambiguous: increasing finish time. Greedy takes, at each step, the compatible
interval with the smallest finish time — that is exactly what "scan in finish
order, take if `s >= last`" does.

*Proof of (E).* Let `S` be optimal with `a(S) = j < k`, written
`S = (g1, …, gj, t, …)`. Greedy's next pick is `g_{j+1}`. Since `t` follows `g_j`
in the compatible set `S`, `start(t) >= finish(g_j)`, so `t` was one of the
candidates greedy was choosing among at step `j+1`; greedy took the minimum
finish, hence

    finish(g_{j+1}) <= finish(t).

First, `g_{j+1} ∉ S \ {g1,…,gj,t}`: if `g_{j+1}` sat later in `S`, then, finishes
in `S` being strictly increasing, `finish(t) < finish(g_{j+1})`, contradicting the
line above. So either `g_{j+1} = t`, and `a(S) >= j+1` already with `S' = S`, or
`g_{j+1}` is absent from `S` and we set

    S' = (S \ {t}) ∪ {g_{j+1}}.

`S'` is feasible: `start(g_{j+1}) >= finish(g_j)` because greedy only picks
compatible intervals, so it fits after the prefix; and every element `u` of `S`
after `t` has `start(u) >= finish(t) >= finish(g_{j+1})`, so it fits after
`g_{j+1}`. `|S'| = |S|` because one element was removed and one distinct element
added, so `val(S') = val(S)`. And `S'` begins `g1, …, gj, g_{j+1}`, so
`a(S') >= j + 1`.

*Proof of (C).* Let `S` be feasible with `a(S) = k`, so `S ⊇ G`. Suppose `S` had a
further element `u`, necessarily with `start(u) >= finish(g_k)`. Then `u` was
compatible with everything greedy had taken when the scan passed it, so greedy
would have taken `u` or some other interval at that point, and would not have
stopped at `k` picks. Contradiction, so `S = G` and `val(S) = val(G)`.

By Part 1, greedy's output is a maximum-cardinality compatible set, and the
answer to *Minimum Removals for Non-Overlapping Intervals* is `n - k`. ∎
:::

Now name the assumptions, because that list is where the bugs live.

- **The swap was one-for-one.** `|S'| = |S|` held because exactly one interval
  left and one arrived. A repair removing two to add one proves nothing; one that
  adds without removing proves `S` was not optimal, so you set the problem up
  wrong.
- **Every interval counts the same.** `val` was cardinality. Attach weights and
  the equality `val(S') = val(S)` becomes `val(S') = val(S) - w(t) + w(g_{j+1})`,
  which can be negative. That is *Meeting Room*, and it is why the answer there is
  a dynamic program and not a sort.
- **Greedy's rule is a genuine minimiser over the current candidates.** The line
  `finish(g_{j+1}) <= finish(t)` is the only place the sort key enters. Sort by
  start, or by length, and that line is simply false — and so is the algorithm.
- **Feasibility depends only on the last finish.** The suffix of `S` was proved
  compatible with `g_{j+1}` using nothing but `finish(g_{j+1}) <= finish(t)`. A
  constraint with more memory ("at most three per day", "no two from the same
  client") breaks this step, not the arithmetic.
- **Ties are harmless here.** The proof only ever used `<=`, so intervals with
  equal finish are interchangeable and the tie-break is free — check that in a new
  problem rather than assuming it.
- **Strict start `<` finish.** This is what made finishes strictly increasing
  inside a compatible set, which is what ruled out `g_{j+1}` hiding later in `S`.
  Zero-length intervals would need the argument patched.

The schema is worth running as code once, because it makes the induction
concrete: start from an optimal solution that looks nothing like greedy's, and
watch it get bent into shape.

```python run
from itertools import combinations


def greedy(ivs):
    out, last = [], float("-inf")
    for iv in sorted(ivs, key=lambda v: (v[1], v[0])):
        if iv[0] >= last:
            out.append(iv)
            last = iv[1]
    return out


def feasible(chosen):
    xs = sorted(chosen)
    return all(xs[i][1] <= xs[i + 1][0] for i in range(len(xs) - 1))


def most_unlike_greedy_optimum(ivs):
    """An optimal solution picked to disagree with greedy as much as possible."""
    for size in range(len(ivs), -1, -1):
        cands = [sorted(c, key=lambda v: (v[1], v[0]))
                 for c in combinations(ivs, size) if feasible(c)]
        if cands:
            return max(cands, key=lambda s: [v[0] for v in s])


ivs = [(1, 4), (2, 4), (0, 6), (4, 7), (5, 8), (7, 10), (8, 11)]
G = greedy(ivs)
S = most_unlike_greedy_optimum(ivs)
print("greedy  G =", G)
print("optimum S =", S, "   same size:", len(S) == len(G))

swaps = 0
while S != G:
    j = next(i for i in range(len(G)) if i >= len(S) or S[i] != G[i])
    t, g = S[j], G[j]
    assert g[1] <= t[1], "greedy's pick must finish no later than S's"
    S2 = S[:j] + [g] + S[j + 1:]
    assert feasible(S2), "obligation 1: still legal"
    assert len(S2) == len(S), "obligation 2: no loss"
    assert S2[:j + 1] == G[:j + 1], "obligation 3: one more agreement"
    swaps += 1
    print("swap %d at position %d: %s -> %s  giving %s" % (swaps, j, t, g, S2))
    S = S2
print("bent into greedy in", swaps, "exchanges; every step stayed optimal")
assert swaps == 3
```

## What it costs

The exchange argument costs nothing at runtime — it is a proof, not a phase. The
first thing to get straight is that its `k` steps are steps of an *induction*.
Beginners sometimes say "the exchange argument makes it `O(n²)`"; nothing is
executed.

What does cost something is the algorithm the argument licenses. For interval
scheduling:

- the sort: `Θ(n log n)` comparisons, and `Θ(n)` extra space for the sorted copy
  that `sorted()` makes;
- the scan: `n` iterations of `O(1)` work — one comparison, one assignment — so
  `Θ(n)`;
- total `T(n) = Θ(n log n) + Θ(n) = Θ(n log n)`, `O(n)` space.

All the cost is in the sort, which tells you how to make it faster. If the
intervals already arrive in finish order — as inside a [[sweep-line]] that has
sorted events anyway — the greedy is `Θ(n)`. If endpoints are small integers,
[[counting-sort]] gives `Θ(n + U)`. You cannot beat `Θ(n log n)` by improving the
*greedy*, because there is no greedy left to improve; comparison sorting alone is
`Ω(n log n)`.

The merge-style greedy behind *Connect N Ropes With Minimum Cost* and *Array
Reduction 1* derives differently. Each move replaces two ropes by one, so there
are exactly `n - 1` moves — a counting argument, not an estimate — and each is two
heap pops and a push on a heap of at most `n` elements, `O(log n)` each:

    T(n) = (n - 1) · O(log n) = Θ(n log n),

with `Θ(n)` space for the heap. Note what the cost *is*: the total paid is
`Σ_leaves length(i) · depth(i)` — every rope's length is paid once for each merge
it takes part in — which is the sentence that makes the greedy obvious and is
also the sentence the exchange argument manipulates.

Two costs people forget.

**The comparator.** When the sort key is a ratio or a concatenation, a comparison
is neither `O(1)` nor automatically correct. Ordering by `a/b` descending should
be cross-multiplied as `a₁·b₂ > a₂·b₁` to avoid float error
([[numerical-stability]]); ordering strings so the concatenation is largest costs
their length per comparison ([[custom-comparators]]).

**The validation.** The brute force you cross-check against enumerates `2ⁿ`
subsets and tests each in `O(n)`: `Θ(2ⁿ · n)`. At `n = 10` that is about 10⁴
operations per instance, so hundreds of instances run instantly; at `n = 25` it is
10⁹ and the interview is gone. Keep the validator's `n` small and its instance
count large — wrong greedies fail on tiny inputs.

## The implementation

```python run
import random
from itertools import combinations


def max_compatible(intervals):
    """A maximum-size set of pairwise non-overlapping intervals.
    Touching is allowed: (1,4) and (4,7) may both stay."""
    kept, last = [], float("-inf")
    for s, f in sorted(intervals, key=lambda iv: (iv[1], iv[0])):
        if s >= last:
            kept.append((s, f))
            last = f
    return kept


def min_removals(intervals):
    return len(intervals) - len(max_compatible(intervals))


def compatible(chosen):
    xs = sorted(chosen)
    return all(xs[i][1] <= xs[i + 1][0] for i in range(len(xs) - 1))


def brute_force(intervals):
    for size in range(len(intervals), -1, -1):
        for sub in combinations(intervals, size):
            if compatible(sub):
                return list(sub)
    return []


demo = [(1, 4), (2, 4), (0, 6), (4, 7), (5, 8), (7, 10), (8, 11)]
print("intervals       ", demo)
print("greedy keeps    ", max_compatible(demo))
print("minimum removals", min_removals(demo))
assert max_compatible(demo) == [(1, 4), (4, 7), (7, 10)]
assert min_removals(demo) == 4

rng = random.Random(4)
for _ in range(300):
    ivs = []
    for _ in range(rng.randint(0, 9)):
        s = rng.randrange(0, 12)
        ivs.append((s, s + rng.randint(1, 5)))
    got = max_compatible(ivs)
    assert compatible(got), ivs
    assert len(got) == len(brute_force(ivs)), ivs
print("300 random instances: greedy matched exhaustive search every time")
```

Three lines carry the argument.

`sorted(intervals, key=lambda iv: (iv[1], iv[0]))` sorts by **finish**, and the
proof's only use of the sort was the inequality `finish(g_{j+1}) <= finish(t)`.
The second component of the key is a tie-break that the proof showed is
irrelevant; it is there so the output is deterministic and tests are reproducible.

`if s >= last` is the feasibility test and the comparator in one character. `>=`
encodes "touching is compatible". Change the problem's convention and this is the
only line that moves.

`last = f` is the entire state. Everything the algorithm remembers about the past
is one number — which is the algorithmic shadow of the proof step that said the
suffix of `S` only ever needed `finish(g_{j+1}) <= finish(t)`.

The random cross-check against `brute_force` is not decoration. It is the cheapest
way to learn that a greedy rule is wrong, and it takes ninety seconds to write.

## Variants you will meet

**Greedy stays ahead.** Instead of swapping, prove by induction that after `i`
decisions greedy's state is at least as good as any solution's — "greedy's `i`-th
jump reaches at least as far", "greedy's `i`-th stop leaves at least as much
fuel". Same induction, exchange left implicit; the natural shape when the state is
one comparable number. *Jump Game II* and *Minimum Refueling Stops* go this way.

**Adjacent swap (the sorting argument).** When the answer is an *order* rather
than a subset you do not need arbitrary exchanges: any permutation becomes any
other by adjacent swaps, so it suffices to show that swapping two adjacent
elements that are out of your chosen order does not hurt. The cost difference of
one adjacent swap is usually two terms, and the comparison that makes it
non-negative *is* your sort key — which is how you discover the key instead of
guessing it. See [[custom-comparators]], and *Biggest Number From Digits* for the
string-concatenation version.

**Structural exchange (Huffman).** Sometimes the exchange is not "swap my choice
for yours" but "rearrange the optimal solution so that my choice becomes
visible". For *Connect N Ropes With Minimum Cost* and *Array Reduction 1*: in any
optimal merge tree, take the two deepest leaves — they are siblings, or can be
made so at no cost — and swap them with the two smallest ropes. Total cost does
not increase, because moving a smaller length deeper and a larger length shallower
changes the total by `(a - b)·(d_b - d_a) <= 0`. Now the two smallest are
siblings, which is exactly greedy's first move, and induction on `n - 1` ropes
finishes it. The full treatment is in [[huffman]].

**Cut-and-exchange on graphs.** Kruskal's rule — take the cheapest edge that
closes no cycle — is proved by exchanging: if an optimal spanning tree omits your
edge, adding it creates a cycle containing an edge you can delete that costs at
least as much. See [[minimum-spanning-tree]] and [[union-find]].

**Exchange as an algorithm.** Occasionally the repair is cheap enough to run at
runtime instead of proving away: decide greedily, and when you overshoot, undo
the worst decision so far with a heap. *Minimum Refueling Stops* is the clean
example — drive as far as you can and, on running dry, retroactively decide you
had stopped at the biggest station you passed. The structure is [[heap]]; the
reason it is correct is this chapter.

### Matroids and when greedy works

There is a class of problems where you do not have to invent the exchange
argument because it is built in. A **matroid** is a finite ground set `E` together
with a family `I` of subsets called independent, such that

1. `∅ ∈ I`;
2. `I` is downward closed: a subset of an independent set is independent;
3. **augmentation**: if `A, B ∈ I` and `|A| < |B|`, there is some `x ∈ B \ A`
   with `A ∪ {x} ∈ I`.

Property 3 is an exchange lemma handed to you for free: whenever some solution is
bigger than what you have, there is an element of it you can absorb. The
Rado–Edmonds theorem says this is exactly the right condition. For a downward
closed set system, the greedy "sort by weight descending, take anything that keeps
the set independent" returns a maximum-weight independent set **for every weight
function if and only if the system is a matroid**.

Examples you already know: forests of a graph (Kruskal); "any `k` elements"
(take the `k` largest); "at most `cᵢ` from group `i`" (a partition matroid — one
mandatory task per day, one item per category); and the sets of unit-length jobs
that can all be finished before their deadlines on one machine, which is the
classic job-sequencing greedy.

Two cautions. Matroids are **sufficient, not necessary**: compatible interval
sets are not a matroid — take `A = {[0,10]}` and `B = {[0,4], [5,9]}`, where
`|A| < |B|` but neither element of `B` can join `A` — and yet this chapter's
greedy is optimal. And the theorem covers *one* matroid: maximising over the
intersection of two is still polynomial but no longer greedy, and over three it
is NP-hard. When you hear "at most one per team, and also within budget", you
have left matroid territory for [[dynamic-programming]] or [[max-flow]].

## Recognising it in a statement

Signals that a greedy with an exchange proof is the intended solution, roughly in
order of reliability:

- **"Maximum number of …" or "minimum number of …" with all items equal.** Unit
  value is what makes the one-for-one swap keep the objective. "Remove the minimum
  number of intervals", "the minimum number of jumps", "the minimum number of
  stops".
- **One resource, consumed in one direction.** Time moving forward, position along
  a line, remaining capacity. If the state after any prefix of decisions is a
  single number, exchanges are cheap to verify.
- **A sum of pairwise-local terms, and the answer is an order.** Reach straight
  for the adjacent-swap argument; the comparator falls out of the algebra.
- **"The largest conflict-free set", where a smaller valid set can always absorb
  from a larger one.** That is a matroid, and greedy by weight needs no thought.
- **Constraints of `10^5` or more with no structure to exploit.** An
  `O(n log n)` sort-then-scan is what fits, and greedy is the usual reason a
  problem that size has a short solution.

The anti-signals matter more than the signals, because they are where confident
people lose marks:

- **Items carry weights unrelated to their footprint.** *Meeting Room* attaches
  `people[i]` to each interval. The shape is identical to the proved problem and
  the greedy is wrong. Weighted interval scheduling is a DP over intervals sorted
  by finish.
- **Two simultaneous budgets.** Capacity *and* count, money *and* time. One swap
  can fix one dimension and break the other — which is the informal reason
  [[knapsack]] is not greedy.
- **A decision's value depends on which other items you picked.** Then the suffix
  of `S` is not interchangeable and the feasibility step of the exchange fails.
- **"Count the ways" or "the number of optimal solutions".** Greedy finds one
  optimum; it does not enumerate. That is [[counting-dp]].

## Traps

**Restating the algorithm and calling it a proof.** "At each step we pick the
interval that finishes earliest, which leaves the most room, so the answer is
optimal." Nothing in that sentence is false and nothing in it is an argument.
Symptom: you cannot name what was exchanged for what. Cure: state obligations
1–3 and discharge them one at a time.

**Bending greedy toward the optimum instead of the other way.** If you start from
`G` and try to improve it into `S`, you prove nothing — of course an optimal
solution is at least as good. The induction only works in the direction that
starts with a perfect solution and shows it survives being made greedier.

**Forgetting that the exchange must preserve feasibility.** The most common hole.
People show the value does not drop and never check that the swapped-in element
does not collide with the rest of the solution.

**Choosing the sort key by vibe.** "Shortest first" feels efficient and is wrong;
"earliest start" feels natural and is wrong. Both are demonstrated below. The
exchange argument is what selects the key: whichever key makes the inequality in
step (E) true is the right one.

**Assuming ties do not matter.** They usually do not, but "usually" is not a
proof, and in a problem with weights or deadlines a tie-break can change the
answer. The proof tells you: if it only ever used `<=`, ties are free.

**Trusting the samples.** Two provided examples cannot tell a right greedy from a
wrong one. A randomised cross-check against brute force on `n <= 10` can, in
seconds.

```python run
from itertools import combinations


def greedy_by(key, ivs):
    kept, last = [], float("-inf")
    for iv in sorted(ivs, key=key):
        if iv[0] >= last:
            kept.append(iv)
            last = iv[1]
    return kept


def ok(chosen):
    xs = sorted(chosen)
    return all(xs[i][1] <= xs[i + 1][0] for i in range(len(xs) - 1))


def best_value(ivs, value):
    out = 0
    for size in range(len(ivs), -1, -1):
        for sub in combinations(ivs, size):
            if ok([(s, f) for s, f, *_ in sub]):
                out = max(out, sum(value(x) for x in sub))
    return out


by_finish = lambda v: (v[1], v[0])
by_start = lambda v: (v[0], v[1])
by_length = lambda v: (v[1] - v[0], v[0])

a = [(1, 4), (2, 4), (0, 6), (4, 7), (5, 8), (7, 10), (8, 11)]
print("A earliest finish:", greedy_by(by_finish, a), "->", len(greedy_by(by_finish, a)))
print("A earliest start :", greedy_by(by_start, a), "->", len(greedy_by(by_start, a)))
assert len(greedy_by(by_finish, a)) == 3 and len(greedy_by(by_start, a)) == 2

b = [(0, 10), (9, 11), (10, 20)]
print("B shortest first :", greedy_by(by_length, b), "->", len(greedy_by(by_length, b)))
print("B earliest finish:", greedy_by(by_finish, b), "->", len(greedy_by(by_finish, b)))
assert len(greedy_by(by_length, b)) == 1 and len(greedy_by(by_finish, b)) == 2

c = [(0, 9, 100), (0, 4, 1), (5, 9, 1)]          # third field: people, as in Meeting Room
picked = greedy_by(by_finish, c)
print("C weighted, earliest finish:", picked, "value", sum(p[2] for p in picked))
print("C true optimum             :", best_value(c, lambda x: x[2]))
assert sum(p[2] for p in picked) == 2 < best_value(c, lambda x: x[2]) == 100
print("counting and weighing are different problems; only one of them is greedy")
```

Instance C is the trap worth staring at. The code is unchanged, the input has one
extra number, and the answer is off by a factor of fifty. Nothing in the
implementation warns you; only the proof does, at the line where `|S'| = |S|`
stopped meaning `val(S') = val(S)`.

## What to memorise

The skeleton, in four lines, which you should be able to say aloud without
notes:

```
Take any optimal S. Let j+1 be the first decision where S differs from greedy.
Replace S's choice there with greedy's.
Show: still feasible; value no worse; agreement up by one.
Agreement is a bounded integer, so repeat until S is greedy. Greedy is optimal.
```

The sentence that turns a problem into it: *"Can I bend any optimal solution one
step toward mine without breaking it or making it worse?"* If the answer is yes
and you can say why, write the greedy. If you cannot say why, the reason is
usually the counterexample.

The habit: **write the exchange before the code, and the brute force after it.**
One sentence of proof and ten lines of random cross-checking against `2ⁿ`
enumeration will catch essentially every wrong greedy rule you will ever invent.

Numbers worth carrying: `2¹⁰ · 10 ≈ 10⁴`, which is why the validator runs at
`n = 10` and not `n = 25`; a sort-and-scan greedy is `Θ(n log n)`, and the scan is
free; a matroid guarantees greedy works for *every* weight function, but greedy
working does not make it a matroid.

## Check yourself

:::check
Why must the exchange argument bend the optimal solution toward greedy, and not
greedy toward the optimal solution?
--
Because the conclusion you need is `val(G) >= OPT`, and you are allowed to assume
only one thing for free: that some optimal solution exists.

Starting from `S` and moving toward `G`, each step preserves optimality (the value
never drops, and it cannot rise above `OPT`), so the endpoint `G` inherits the
value `OPT`. Starting from `G` and improving toward `S` shows only that `S` is at
least as good as `G` — which is the definition of `S` being optimal, and says
nothing about `G`.

Put differently: the argument proves that the set of optimal solutions *contains*
greedy's, by walking inside that set. You must stay inside it the whole way, which
is only possible if you start inside it.
:::

:::check
Someone says: "greedy is provably correct exactly when the problem is a matroid."
Where are they wrong, and what is the true statement?
--
They have turned a sufficient condition into a characterisation.

The true statement, Rado–Edmonds, is narrower than it sounds: for a **downward
closed set system**, greedy by weight is optimal **for every weight function** if
and only if the system is a matroid. The quantifier is doing the work. A given
problem can have a non-matroid structure and a greedy that is still optimal for
the one objective it actually has.

Interval scheduling is the counterexample. Compatible sets are downward closed,
but augmentation fails: `A = {[0,10]}` and `B = {[0,4], [5,9]}` have `|A| < |B|`
and neither element of `B` can be added to `A`. So it is not a matroid — and the
proof in this chapter still shows the earliest-finish greedy is optimal, because
that proof exchanges in a way the matroid axioms do not describe.

Matroids are the case where you do not have to think. The exchange argument is
what you use when you do.
:::

:::check
*Meeting Room* is the interval problem with a number of people attached to each
group, and you must minimise the people who cannot meet. Point at the exact line
of the proof that fails, and say what it tells you to write instead.
--
The line `|S'| = |S|, so val(S') = val(S)` in the proof of (E).

With weights, removing `t` and inserting `g_{j+1}` changes the objective by
`w(g_{j+1}) - w(t)`, and greedy's rule (earliest finish) says nothing about
weights, so that difference can be very negative. Instance C in the traps block
is the minimal example: a single group of 100 loses to two groups of 1 because
the two finish earlier.

The failure is informative: the value of a decision is not determined by the
resource it consumes, so the future cannot be summarised by `last` alone. You need,
for each interval, the best value among all schedules ending at or before its
start — weighted interval scheduling: sort by finish,
`best[i] = max(best[i-1], w[i] + best[p(i)])` where `p(i)` is found by
[[binary-search]], `O(n log n)` — the same complexity, a different algorithm, and
the reason worth knowing is that the proof, not the code, told you to switch.
:::

:::check
*Connect N Ropes With Minimum Cost* pays the sum of the two ropes it joins. Why
may you assume that some optimal solution joins the two shortest ropes first?
--
Because of a structural exchange on the merge tree. Any sequence of merges is a
binary tree whose leaves are the ropes, and the total paid is
`Σ length(i) · depth(i)`: a rope's length is paid once for every merge it takes
part in.

Take an optimal tree and look at a deepest internal node: its two children are
leaves, and no leaf is deeper. Let `a` be one of the two shortest ropes and `x`
one of those deepest leaves. Swapping their positions changes the cost by
`(length(a) - length(x)) · (depth(x) - depth(a))`. The first factor is `<= 0`
because `a` is among the shortest; the second is `>= 0` because `x` is among the
deepest; so the product is `<= 0` and the cost does not increase. Do it for both shortest ropes and you have an optimal tree in
which they are siblings at the bottom — an optimal solution whose first merge is
greedy's. Replace that pair by one rope of their combined length and induct on
`n - 1` ropes; the merge you just fixed is paid exactly once, so the recursion is
on the same objective. *Array Reduction 1* is this argument with a different
story.
:::

:::check
In the worked trace, greedy skipped `(0,6)` even though it was legal to take at
that moment. Construct the general rule this illustrates, and explain why the
proof needs it.
--
The rule: among all intervals compatible with what you have taken, take the one
with the **smallest finish**, not the first that fits. "Fits" is a property of the
interval; "leaves the most room" is a property of the future, and only the second
is being optimised.

The proof needs it at exactly one line: `finish(g_{j+1}) <= finish(t)`, where `t`
is whatever the optimum chose at that position. Greedy's pick is the minimiser
over the candidate set and `t` belongs to that set, so the inequality is
immediate — and everything later rests on it, because the suffix of `S`, which was
compatible with `t`, is compatible with `g_{j+1}` only by finishing no later.

If you picked by earliest start instead, `t` is still a candidate but greedy's
pick may finish much later, the inequality reverses, and the suffix of `S` may
collide with your choice. That is not a theoretical gap: on the traced instance,
earliest-start keeps two intervals where three are possible.
:::

:::check
You have invented a greedy rule for a new problem and have twenty minutes left.
You cannot see how to prove it. What is the most efficient use of the next three
minutes, and why?
--
Write the brute force and cross-check on random tiny inputs.

An exhaustive search over `2ⁿ` subsets or `n!` orders at `n <= 8` is ten lines and
runs instantly, and a few hundred random instances disagree with a wrong greedy
almost immediately — wrong rules fail on small awkward inputs, not on large ones.
A disagreement hands you a minimal counterexample, which is both a refutation and
usually the hint for the correct rule; agreement over hundreds of instances is no
proof, but it is enough to commit code to.

Proving first is the wrong order for a rule you doubt: you will spend the twenty
minutes discovering the exchange step is false, which is what the test tells you
in three, with a concrete example attached. Prove second, once you believe the
rule. See [[testing-your-code]].
:::
